import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from database import db
from models.student import Student
from models.course import Course
from models.grade import Grade


upload_bp = Blueprint(
    "upload",
    __name__
)


@upload_bp.route("/upload", methods=["GET"])
def upload_page():

    return render_template(
        "upload.html"
    )


@upload_bp.route("/upload", methods=["POST"])
def upload_csv():

    file = request.files.get("file")

    if not file:
        return "Please select a CSV file", 400

    if file.filename == "":
        return "Please select a CSV file", 400

    if not file.filename.lower().endswith(".csv"):
        return "Only CSV files are allowed", 400

    try:

        df = pd.read_csv(file)

        required_columns = [
            "student_name",
            "student_email",
            "course_name",
            "course_code",
            "score",
            "date"
        ]

        for column in required_columns:

            if column not in df.columns:
                return (
                    f"Missing required column: {column}",
                    400
                )

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            student_name = str(
                row["student_name"]
            ).strip()

            student_email = str(
                row["student_email"]
            ).strip()

            course_name = str(
                row["course_name"]
            ).strip()

            course_code = str(
                row["course_code"]
            ).strip()

            # Validate score
            try:
                score = float(row["score"])
            except (ValueError, TypeError):
                skipped += 1
                continue

            if score < 0 or score > 100:
                skipped += 1
                continue

            # Validate date
            try:
                grade_date = pd.to_datetime(
                    row["date"]
                ).date()
            except Exception:
                skipped += 1
                continue

            # Find student
            student = Student.query.filter_by(
                email=student_email
            ).first()

            # Create student if not found
            if not student:

                student = Student(
                    name=student_name,
                    email=student_email
                )

                db.session.add(student)
                db.session.flush()

            # Find course
            course = Course.query.filter_by(
                code=course_code
            ).first()

            # Create course if not found
            if not course:

                course = Course(
                    name=course_name,
                    code=course_code
                )

                db.session.add(course)
                db.session.flush()

            # Create grade
            grade = Grade(
                student_id=student.id,
                course_id=course.id,
                score=score,
                date=grade_date
            )

            db.session.add(grade)

            inserted += 1

        db.session.commit()

        return (
            f"{inserted} grades uploaded successfully. "
            f"{skipped} rows skipped. "
            f"<br><br>"
            f"<a href='{url_for('grade_web.grades_page')}'>"
            f"View Grades"
            f"</a>"
        )

    except Exception as e:

        db.session.rollback()

        return (
            f"Error processing CSV: {e}",
            400
        )