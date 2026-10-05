from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from database import db
from models.course import Course


course_bp = Blueprint("course", __name__)


# GET /api/courses
@course_bp.route("/api/courses", methods=["GET"])
@jwt_required()
def get_courses():

    courses = Course.query.all()

    course_list = []

    for course in courses:
        course_list.append({
            "id": course.id,
            "name": course.name,
            "code": course.code
        })

    return jsonify(course_list), 200


# POST /api/courses
@course_bp.route("/api/courses", methods=["POST"])
@jwt_required()
def create_course():

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
    code = data.get("code")

    if not name or not code:
        return jsonify({
            "message": "Course name and code are required"
        }), 400

    existing_course = Course.query.filter_by(code=code).first()

    if existing_course:
        return jsonify({
            "message": "Course with this code already exists"
        }), 409

    course = Course(
        name=name,
        code=code
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "course": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 201


# GET /api/courses/<id>
@course_bp.route("/api/courses/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):

    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    return jsonify({
        "id": course.id,
        "name": course.name,
        "code": course.code
    }), 200


# PUT /api/courses/<id>
@course_bp.route("/api/courses/<int:course_id>", methods=["PUT"])
@jwt_required()
def update_course(course_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    code = data.get("code")

    if not name or not code:
        return jsonify({
            "message": "Name and code are required for PUT"
        }), 400

    existing_course = Course.query.filter(
        Course.code == code,
        Course.id != course_id
    ).first()

    if existing_course:
        return jsonify({
            "message": "Another course already uses this code"
        }), 409

    course.name = name
    course.code = code

    db.session.commit()

    return jsonify({
        "message": "Course updated successfully",
        "course": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 200


# PATCH /api/courses/<id>
@course_bp.route("/api/courses/<int:course_id>", methods=["PATCH"])
@jwt_required()
def patch_course(course_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "name" in data:
        if not data["name"]:
            return jsonify({
                "message": "Course name cannot be empty"
            }), 400

        course.name = data["name"]

    if "code" in data:

        if not data["code"]:
            return jsonify({
                "message": "Course code cannot be empty"
            }), 400

        existing_course = Course.query.filter(
            Course.code == data["code"],
            Course.id != course_id
        ).first()

        if existing_course:
            return jsonify({
                "message": "Another course already uses this code"
            }), 409

        course.code = data["code"]

    db.session.commit()

    return jsonify({
        "message": "Course partially updated successfully",
        "course": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 200


# DELETE /api/courses/<id>
@course_bp.route("/api/courses/<int:course_id>", methods=["DELETE"])
@jwt_required()
def delete_course(course_id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "message": "Admin access required"
        }), 403

    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully"
    }), 200