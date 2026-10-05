from flask import Blueprint, render_template, request, redirect, url_for

from database import db
from models.grade import Grade
from models.student import Student
from models.course import Course

grade_web_bp = Blueprint("grade_web", __name__)


# =========================
# LIST GRADES
# =========================
@grade_web_bp.route("/grades", methods=["GET"])
def grades_page():
    grades = Grade.query.all()

    return render_template(
        "grades.html",
        grades=grades
    )


# =========================
# ADD GRADE FORM
# =========================
@grade_web_bp.route("/grades/new", methods=["GET"])
def new_grade_page():
    students = Student.query.all()
    courses = Course.query.all()

    return render_template(
        "grade_form.html",
        students=students,
        courses=courses
    )


# =========================
# CREATE GRADE
# =========================
@grade_web_bp.route("/grades", methods=["POST"])
def create_grade():

    student_id = request.form.get("student_id")
    course_id = request.form.get("course_id")
    score = request.form.get("score")
    grade_date = request.form.get("date")

    if not student_id or not course_id or not score or not grade_date:
        return "All grade fields are required", 400

    try:
        score = float(score)
    except ValueError:
        return "Score must be a number", 400

    if score < 0 or score > 100:
        return "Score must be between 0 and 100", 400

    student = Student.query.get(student_id)

    if not student:
        return "Student not found", 404

    course = Course.query.get(course_id)

    if not course:
        return "Course not found", 404

    grade = Grade(
        student_id=student_id,
        course_id=course_id,
        score=score,
        date=grade_date
    )

    db.session.add(grade)
    db.session.commit()

    return redirect(
        url_for("grade_web.grades_page")
    )


# =========================
# GRADE DETAILS
# =========================
@grade_web_bp.route("/grades/<int:grade_id>", methods=["GET"])
def grade_detail(grade_id):

    grade = Grade.query.get(grade_id)

    if not grade:
        return "Grade not found", 404

    return render_template(
        "grade_detail.html",
        grade=grade
    )


# =========================
# EDIT GRADE FORM
# =========================
@grade_web_bp.route("/grades/<int:grade_id>/edit", methods=["GET"])
def edit_grade_page(grade_id):

    grade = Grade.query.get(grade_id)

    if not grade:
        return "Grade not found", 404

    students = Student.query.all()
    courses = Course.query.all()

    return render_template(
        "grade_edit.html",
        grade=grade,
        students=students,
        courses=courses
    )


# =========================
# UPDATE GRADE
# =========================
@grade_web_bp.route(
    "/grades/<int:grade_id>",
    methods=["PUT", "POST"]
)
def update_grade(grade_id):

    if request.method == "POST":

        method = request.form.get("_method", "").upper()

        if method != "PUT":
            return "Invalid method override", 405

    grade = Grade.query.get(grade_id)

    if not grade:
        return "Grade not found", 404

    student_id = request.form.get("student_id")
    course_id = request.form.get("course_id")
    score = request.form.get("score")
    grade_date = request.form.get("date")

    if not student_id or not course_id or not score or not grade_date:
        return "All grade fields are required", 400

    try:
        score = float(score)
    except ValueError:
        return "Score must be a number", 400

    if score < 0 or score > 100:
        return "Score must be between 0 and 100", 400

    student = Student.query.get(student_id)

    if not student:
        return "Student not found", 404

    course = Course.query.get(course_id)

    if not course:
        return "Course not found", 404

    grade.student_id = student_id
    grade.course_id = course_id
    grade.score = score
    grade.date = grade_date

    db.session.commit()

    return redirect(
        url_for(
            "grade_web.grade_detail",
            grade_id=grade.id
        )
    )


# =========================
# DELETE GRADE
# =========================
@grade_web_bp.route(
    "/grades/<int:grade_id>",
    methods=["DELETE", "POST"]
)
def delete_grade(grade_id):

    if request.method == "POST":

        method = request.form.get("_method", "").upper()

        if method != "DELETE":
            return "Invalid method override", 405

    grade = Grade.query.get(grade_id)

    if not grade:
        return "Grade not found", 404

    db.session.delete(grade)
    db.session.commit()

    return redirect(
        url_for("grade_web.grades_page")
    )