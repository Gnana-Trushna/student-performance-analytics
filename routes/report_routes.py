from flask import Blueprint, Response, send_file

from services.report_service import (
    create_csv_report,
    create_excel_report
)

report_bp = Blueprint("reports", __name__)


@report_bp.route("/reports/grades.csv", methods=["GET"])
def grades_csv():

    csv_data = create_csv_report()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=grades_report.csv"
        }
    )


@report_bp.route("/reports/grades.xlsx", methods=["GET"])
def grades_excel():

    excel_file = create_excel_report()

    return send_file(
        excel_file,
        as_attachment=True,
        download_name="grades_report.xlsx",
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )