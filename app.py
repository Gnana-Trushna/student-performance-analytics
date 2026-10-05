from flask import Flask, render_template
from io import BytesIO
from urllib.parse import parse_qs
from sqlalchemy import text
from flask_jwt_extended import JWTManager

from config import Config
from database import db

# Import models so SQLAlchemy knows about them
from models.user import User
from models.student import Student
from models.course import Course
from models.grade import Grade

# Import API route blueprints
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.course_routes import course_bp
from routes.grade_routes import grade_bp

# Import Web route blueprints
from routes.student_web_routes import student_web_bp
from routes.course_web_routes import course_web_bp

from routes.grade_web_routes import grade_web_bp

from routes.analytics_routes import analytics_bp

from routes.report_routes import report_bp

from routes.upload_routes import upload_bp
# ============================================================
# METHOD OVERRIDE MIDDLEWARE
# ============================================================

class MethodOverrideMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        # HTML forms normally submit using POST.
        # Check whether the form wants PUT, PATCH, or DELETE.
        if environ.get("REQUEST_METHOD") == "POST":

            content_length = environ.get("CONTENT_LENGTH")

            if content_length:

                try:
                    length = int(content_length)
                except ValueError:
                    length = 0

                body = environ["wsgi.input"].read(length)

                # Parse the submitted form data
                form_data = parse_qs(
                    body.decode("utf-8")
                )

                # Read the hidden _method field
                method = form_data.get(
                    "_method",
                    [""]
                )[0].upper()

                # Allow only the methods required by the assignment
                if method in ["PUT", "PATCH", "DELETE"]:

                    environ["REQUEST_METHOD"] = method

                # Put the body back so Flask can read request.form
                environ["wsgi.input"] = BytesIO(body)

        return self.app(environ, start_response)


# ============================================================
# CREATE FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# Enable method override BEFORE Flask handles the request
app.wsgi_app = MethodOverrideMiddleware(app.wsgi_app)


# ============================================================
# LOAD CONFIGURATION
# ============================================================

app.config.from_object(Config)


# ============================================================
# CONNECT SQLALCHEMY TO FLASK
# ============================================================

db.init_app(app)


# ============================================================
# CONFIGURE JWT
# ============================================================

jwt = JWTManager(app)


# ============================================================
# REGISTER API BLUEPRINTS
# ============================================================

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(course_bp)
app.register_blueprint(grade_bp)


# ============================================================
# REGISTER WEB BLUEPRINTS
# ============================================================

app.register_blueprint(student_web_bp)
app.register_blueprint(course_web_bp)

app.register_blueprint(grade_web_bp)

app.register_blueprint(analytics_bp)

app.register_blueprint(report_bp)

app.register_blueprint(upload_bp)
# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():
    return render_template("home.html")

# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

@app.route("/test-db")
def test_db():

    try:

        with db.engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            value = result.scalar()

        return (
            f"MySQL connection successful! "
            f"Test result: {value}"
        )

    except Exception as e:

        return f"MySQL connection failed: {e}"


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

@app.route("/create-tables")
def create_tables():

    try:

        with app.app_context():

            db.create_all()

        return "Database tables created successfully!"

    except Exception as e:

        return f"Error creating tables: {e}"


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)