from flask import Blueprint, render_template, request, redirect, url_for

from database import db
from models.course import Course


course_web_bp = Blueprint("course_web", __name__)

# COURSE LIST

@course_web_bp.route("/courses", methods=["GET"])
def courses_page():

    courses = Course.query.all()

    return render_template(
        "courses.html",
        courses=courses
    )

# ADD COURSE PAGE


@course_web_bp.route("/courses/new", methods=["GET"])
def new_course_page():

    return render_template("course_form.html")


# CREATE COURSE

@course_web_bp.route("/courses", methods=["POST"])
def create_course():

    name = request.form.get("name")
    code = request.form.get("code")

    if not name or not code:
        return "Course name and code are required", 400

    existing_course = Course.query.filter_by(
        code=code
    ).first()

    if existing_course:
        return "A course with this code already exists", 400

    course = Course(
        name=name,
        code=code
    )

    db.session.add(course)
    db.session.commit()

    return redirect(
        url_for("course_web.courses_page")
    )


# COURSE DETAIL

@course_web_bp.route(
    "/courses/<int:course_id>",
    methods=["GET"]
)
def course_detail(course_id):

    course = Course.query.get(course_id)

    if not course:
        return "Course not found", 404

    return render_template(
        "course_detail.html",
        course=course
    )


# EDIT COURSE PAGE

@course_web_bp.route(
    "/courses/<int:course_id>/edit",
    methods=["GET"]
)
def edit_course_page(course_id):

    course = Course.query.get(course_id)

    if not course:
        return "Course not found", 404

    return render_template(
        "course_edit.html",
        course=course
    )

# UPDATE COURSE


@course_web_bp.route(
    "/courses/<int:course_id>",
    methods=["PUT", "POST"]
)
def update_course(course_id):

    # If this is a POST, check the method override field.
    if request.method == "POST":

        method = request.form.get(
            "_method",
            ""
        ).upper()

        if method != "PUT":
            return "Invalid method override", 405

    course = Course.query.get(course_id)

    if not course:
        return "Course not found", 404

    name = request.form.get("name")
    code = request.form.get("code")

    if not name or not code:
        return "Course name and code are required", 400

    existing_course = Course.query.filter(
        Course.code == code,
        Course.id != course_id
    ).first()

    if existing_course:
        return "A course with this code already exists", 400

    course.name = name
    course.code = code

    db.session.commit()

    return redirect(
        url_for(
            "course_web.course_detail",
            course_id=course.id
        )
    )


# DELETE COURSE

@course_web_bp.route(
    "/courses/<int:course_id>",
    methods=["DELETE", "POST"]
)
def delete_course(course_id):

    # If browser sends POST, verify that the form requested DELETE.
    if request.method == "POST":

        method = request.form.get(
            "_method",
            ""
        ).upper()

        if method != "DELETE":
            return "Invalid method override", 405

    course = Course.query.get(course_id)

    if not course:
        return "Course not found", 404

    db.session.delete(course)
    db.session.commit()

    return redirect(
        url_for("course_web.courses_page")
    )