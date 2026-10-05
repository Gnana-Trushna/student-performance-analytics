from app import app
from database import db
from models.user import User
from werkzeug.security import generate_password_hash


with app.app_context():

    # Check whether admin already exists
    existing_admin = User.query.filter_by(
        email="admin@example.com"
    ).first()

    if existing_admin:
        print("Admin user already exists.")

    else:
        admin = User(
            name="Admin",
            email="admin@example.com",
            password=generate_password_hash("Admin@123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully!")