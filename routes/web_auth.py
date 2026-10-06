from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from database import db
from models.user import User


web_auth_bp = Blueprint("web_auth", __name__)


@web_auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Show login page
    if request.method == "GET":
        return render_template("login.html")

    # Get form data
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return render_template(
            "login.html",
            error="Email and password are required"
        )

    # Find user
    user = User.query.filter_by(email=email).first()

    if not user:
        return render_template(
            "login.html",
            error="Invalid email or password"
        )

    # Check password
    if not check_password_hash(user.password, password):
        return render_template(
            "login.html",
            error="Invalid email or password"
        )

    # Store login information in browser session
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["user_role"] = user.role
    session["user_email"] = user.email

    # Redirect based on role
    if user.role == "admin":
        return redirect(url_for("student_web.students_page"))

    return redirect(url_for("grade.my_grades"))


@web_auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("web_auth.login"))