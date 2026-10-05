from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from database import db
from models.student import Student


student_bp = Blueprint("student", __name__)


# GET /api/students
@student_bp.route("/api/students", methods=["GET"])
@jwt_required()
def get_students():

    students = Student.query.all()

    student_list = []

    for student in students:
        student_list.append({
            "id": student.id,
            "name": student.name,
            "email": student.email
        })

    return jsonify(student_list), 200


# POST /api/students
@student_bp.route("/api/students", methods=["POST"])
@jwt_required()
def create_student():

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

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "message": "Name and email are required"
        }), 400

    existing_student = Student.query.filter_by(email=email).first()

    if existing_student:
        return jsonify({
            "message": "Student with this email already exists"
        }), 409

    student = Student(
        name=name,
        email=email
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 201


# GET /api/students/<id>
@student_bp.route("/api/students/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "id": student.id,
        "name": student.name,
        "email": student.email
    }), 200


# PUT /api/students/<id>
@student_bp.route("/api/students/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "message": "Name and email are required for PUT"
        }), 400

    existing_student = Student.query.filter(
        Student.email == email,
        Student.id != student_id
    ).first()

    if existing_student:
        return jsonify({
            "message": "Another student already uses this email"
        }), 409

    student.name = name
    student.email = email

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 200


# PATCH /api/students/<id>
@student_bp.route("/api/students/<int:student_id>", methods=["PATCH"])
@jwt_required()
def patch_student(student_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "name" in data:
        student.name = data["name"]

    if "email" in data:

        existing_student = Student.query.filter(
            Student.email == data["email"],
            Student.id != student_id
        ).first()

        if existing_student:
            return jsonify({
                "message": "Another student already uses this email"
            }), 409

        student.email = data["email"]

    db.session.commit()

    return jsonify({
        "message": "Student partially updated successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 200


# DELETE /api/students/<id>
@student_bp.route("/api/students/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    }), 200