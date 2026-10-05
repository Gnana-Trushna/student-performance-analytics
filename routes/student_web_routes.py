from flask import Blueprint, render_template, request, redirect, url_for

from database import db
from models.student import Student


student_web_bp = Blueprint("student_web", __name__)


@student_web_bp.route("/students", methods=["GET"])
def students_page():

    search = request.args.get("search", "").strip()

    if search:
        students = Student.query.filter(
            db.or_(
                Student.name.ilike(f"%{search}%"),
                Student.email.ilike(f"%{search}%")
            )
        ).all()
    else:
        students = Student.query.all()

    return render_template(
        "students.html",
        students=students,
        search=search
    )


@student_web_bp.route("/students/new", methods=["GET"])
def new_student_page():

    return render_template("student_form.html")


@student_web_bp.route("/students", methods=["POST"])
def create_student():

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Name and email are required", 400

    existing_student = Student.query.filter_by(
        email=email
    ).first()

    if existing_student:
        return "A student with this email already exists", 400

    student = Student(
        name=name,
        email=email
    )

    db.session.add(student)
    db.session.commit()

    return redirect(url_for("student_web.students_page"))

@student_web_bp.route("/students/<int:student_id>", methods=["GET"])
def student_detail(student_id):

    student = Student.query.get(student_id)

    if not student:
        return "Student not found", 404

    return render_template(
        "student_detail.html",
        student=student
    )

@student_web_bp.route("/students/<int:student_id>/edit", methods=["GET"])
def edit_student_page(student_id):

    student = Student.query.get(student_id)

    if not student:
        return "Student not found", 404

    return render_template(
        "student_edit.html",
        student=student
    )

@student_web_bp.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        return "Student not found", 404

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Name and email are required", 400

    existing_student = Student.query.filter(
        Student.email == email,
        Student.id != student_id
    ).first()

    if existing_student:
        return "A student with this email already exists", 400

    student.name = name
    student.email = email

    db.session.commit()

    return redirect(
        url_for(
            "student_web.student_detail",
            student_id=student.id
        )
    )

@student_web_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        return "Student not found", 404

    db.session.delete(student)
    db.session.commit()

    return redirect(
        url_for("student_web.students_page")
    )