from functools import wraps

from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)


def admin_required(fn):

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if claims.get("role") != "admin":

            return jsonify({
                "message": "Admin access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper


def student_required(fn):

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if claims.get("role") != "student":

            return jsonify({
                "message": "Student access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper