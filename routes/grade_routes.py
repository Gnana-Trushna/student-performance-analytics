from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from models.grade import Grade
from models.student import Student
from models.course import Course
from models.user import User


grade_bp = Blueprint("grade", __name__)


# GET /api/grades
@grade_bp.route("/api/grades", methods=["GET"])
@jwt_required()
def get_grades():

    grades = Grade.query.all()

    grade_list = []

    for grade in grades:
        grade_list.append({
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": str(grade.date)
        })

    return jsonify(grade_list), 200


# POST /api/grades
@grade_bp.route("/api/grades", methods=["POST"])
@jwt_required()
def create_grade():

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    score = data.get("score")

    if student_id is None or course_id is None or score is None:
        return jsonify({
            "message": "student_id, course_id and score are required"
        }), 400

    # Check student
    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    # Check course
    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    # Validate score
    if score < 0 or score > 100:
        return jsonify({
            "message": "Score must be between 0 and 100"
        }), 400

    grade = Grade(
        student_id=student_id,
        course_id=course_id,
        score=score
    )

    db.session.add(grade)
    db.session.commit()

    return jsonify({
        "message": "Grade created successfully",
        "grade": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": str(grade.date)
        }
    }), 201


# GET /api/grades/<id>
@grade_bp.route("/api/grades/<int:grade_id>", methods=["GET"])
@jwt_required()
def get_grade(grade_id):

    grade = Grade.query.get(grade_id)

    if not grade:
        return jsonify({
            "message": "Grade not found"
        }), 404

    return jsonify({
        "id": grade.id,
        "student_id": grade.student_id,
        "course_id": grade.course_id,
        "score": grade.score,
        "date": str(grade.date)
    }), 200


# PUT /api/grades/<id>
@grade_bp.route("/api/grades/<int:grade_id>", methods=["PUT"])
@jwt_required()
def update_grade(grade_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    grade = Grade.query.get(grade_id)

    if not grade:
        return jsonify({
            "message": "Grade not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    score = data.get("score")

    if student_id is None or course_id is None or score is None:
        return jsonify({
            "message": "student_id, course_id and score are required for PUT"
        }), 400

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    if score < 0 or score > 100:
        return jsonify({
            "message": "Score must be between 0 and 100"
        }), 400

    grade.student_id = student_id
    grade.course_id = course_id
    grade.score = score

    db.session.commit()

    return jsonify({
        "message": "Grade updated successfully",
        "grade": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": str(grade.date)
        }
    }), 200


# PATCH /api/grades/<id>
@grade_bp.route("/api/grades/<int:grade_id>", methods=["PATCH"])
@jwt_required()
def patch_grade(grade_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    grade = Grade.query.get(grade_id)

    if not grade:
        return jsonify({
            "message": "Grade not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "student_id" in data:

        student = Student.query.get(data["student_id"])

        if not student:
            return jsonify({
                "message": "Student not found"
            }), 404

        grade.student_id = data["student_id"]

    if "course_id" in data:

        course = Course.query.get(data["course_id"])

        if not course:
            return jsonify({
                "message": "Course not found"
            }), 404

        grade.course_id = data["course_id"]

    if "score" in data:

        score = data["score"]

        if score < 0 or score > 100:
            return jsonify({
                "message": "Score must be between 0 and 100"
            }), 400

        grade.score = score

    db.session.commit()

    return jsonify({
        "message": "Grade partially updated successfully",
        "grade": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": str(grade.date)
        }
    }), 200


# DELETE /api/grades/<id>
@grade_bp.route("/api/grades/<int:grade_id>", methods=["DELETE"])
@jwt_required()
def delete_grade(grade_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    grade = Grade.query.get(grade_id)

    if not grade:
        return jsonify({
            "message": "Grade not found"
        }), 404

    db.session.delete(grade)
    db.session.commit()

    return jsonify({
        "message": "Grade deleted successfully"
    }), 200

@grade_bp.route("/grades/my", methods=["GET"])
@jwt_required()
def my_grades():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return {
            "message": "User not found"
        }, 404

    grades = Grade.query.filter_by(
        student_id=user.id
    ).all()

    result = []

    for grade in grades:

        result.append({
            "id": grade.id,
            "student": grade.student.name,
            "course": grade.course.name,
            "course_code": grade.course.code,
            "score": grade.score,
            "date": str(grade.date)
        })

    return {
        "grades": result
    }, 200