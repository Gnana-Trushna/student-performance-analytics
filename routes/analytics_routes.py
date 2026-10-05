from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np

from models.grade import Grade

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics", methods=["GET"])
def analytics_page():

    grades = Grade.query.all()

    if not grades:
        return render_template(
            "analytics.html",
            has_data=False
        )

    # Convert database records into a list of dictionaries
    data = []

    for grade in grades:
        data.append({
            "student_id": grade.student_id,
            "student_name": grade.student.name,
            "course_id": grade.course_id,
            "course_name": grade.course.name,
            "score": grade.score,
            "date": grade.date
        })

    # Create Pandas DataFrame
    df = pd.DataFrame(data)

    # Optional filters
    student_filter = request.args.get(
        "student",
        ""
    ).strip()

    course_filter = request.args.get(
        "course",
        ""
    ).strip()

    if student_filter:
        df = df[
            df["student_name"].str.contains(
                student_filter,
                case=False,
                na=False
            )
        ]

    if course_filter:
        df = df[
            df["course_name"].str.contains(
                course_filter,
                case=False,
                na=False
            )
        ]

    if df.empty:
        return render_template(
            "analytics.html",
            has_data=False,
            student_filter=student_filter,
            course_filter=course_filter
        )

    # NumPy score array
    scores = df["score"].to_numpy(dtype=float)

    # Overall statistics
    overall_mean = np.mean(scores)
    overall_median = np.median(scores)
    overall_std = np.std(scores)

    # Course-wise average
    course_average = (
        df.groupby("course_name")["score"]
        .mean()
        .reset_index()
    )

    course_average.columns = [
        "course_name",
        "average_score"
    ]

    # Student ranking
    student_ranking = (
        df.groupby(
            ["student_id", "student_name"]
        )["score"]
        .mean()
        .reset_index()
    )

    student_ranking.columns = [
        "student_id",
        "student_name",
        "average_score"
    ]

    student_ranking = student_ranking.sort_values(
        by="average_score",
        ascending=False
    )

    # Add rank
    student_ranking["rank"] = (
        student_ranking["average_score"]
        .rank(
            method="min",
            ascending=False
        )
        .astype(int)
    )

    # Convert DataFrames into records for Jinja
    course_average_records = (
        course_average
        .round(2)
        .to_dict(orient="records")
    )

    student_ranking_records = (
        student_ranking
        .round(2)
        .to_dict(orient="records")
    )

    grade_records = (
        df
        .sort_values("date", ascending=False)
        .to_dict(orient="records")
    )

    return render_template(
        "analytics.html",

        has_data=True,

        overall_mean=round(
            float(overall_mean),
            2
        ),

        overall_median=round(
            float(overall_median),
            2
        ),

        overall_std=round(
            float(overall_std),
            2
        ),

        course_average=course_average_records,

        student_ranking=student_ranking_records,

        grade_records=grade_records,

        student_filter=student_filter,

        course_filter=course_filter
    )