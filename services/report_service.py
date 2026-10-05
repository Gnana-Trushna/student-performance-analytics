import pandas as pd

from models.grade import Grade


def get_grade_dataframe():

    grades = Grade.query.all()

    data = []

    for grade in grades:
        data.append({
            "Grade ID": grade.id,
            "Student": grade.student.name,
            "Student Email": grade.student.email,
            "Course": grade.course.name,
            "Course Code": grade.course.code,
            "Score": grade.score,
            "Date": grade.date
        })

    return pd.DataFrame(data)


def create_csv_report():

    df = get_grade_dataframe()

    return df.to_csv(index=False)


def create_excel_report():

    df = get_grade_dataframe()

    from io import BytesIO

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Grades"
        )

    output.seek(0)

    return output