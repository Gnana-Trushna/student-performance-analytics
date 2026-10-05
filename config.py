from sqlalchemy.engine import URL


class Config:
    DB_USERNAME = "root"
    DB_PASSWORD = "SECRET"
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "student_performance_db"

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "change-this-secret-key"