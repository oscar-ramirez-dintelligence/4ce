from flask import render_template, request, session, make_response
from . import bp
from cotizador.services import reporte_service
import io
import csv

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the main reporting interface.
    Handles form submission to generate and display a report.
    """
    report_data = None
    headers = None

    if request.method == 'POST':
        report_type = request.form.get('report_type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        headers, report_data = reporte_service.generate_report(report_type, start_date, end_date)

        # Store report data in session to be used for CSV download
        session['last_report_data'] = report_data
        session['last_report_headers'] = headers
        session['last_report_name'] = f"{report_type}_{start_date}_to_{end_date}"

    return render_template(
        'reportes/index.html',
        headers=headers,
        report_data=report_data
    )

@bp.route('/download-report')
def download_report():
    """
    Takes the last generated report data from the session and returns it as a CSV file.
    """
    report_data = session.get('last_report_data')
    headers = session.get('last_report_headers')
    report_name = session.get('last_report_name', 'reporte')

    if not report_data or not headers:
        return "No hay datos de reporte para descargar.", 404

    # Use io.StringIO to create a file in memory
    si = io.StringIO()
    cw = csv.writer(si)

    # Write headers
    cw.writerow(headers)
    # Write data rows
    for row_dict in report_data:
        cw.writerow([row_dict.get(h) for h in headers])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={report_name}.csv"
    output.headers["Content-type"] = "text/csv"

    return output
