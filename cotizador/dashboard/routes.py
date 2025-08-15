from flask import render_template
from . import bp
from cotizador.services import dashboard_service

@bp.route('/')
def main_dashboard():
    """
    Renders the main sales dashboard page.
    """
    # Fetch all the data needed for the dashboard from the service layer
    metrics = dashboard_service.get_dashboard_metrics()
    monthly_sales = dashboard_service.get_monthly_sales_data()
    active_reservations = dashboard_service.get_active_reservations_data()

    return render_template(
        'dashboard/dashboard.html',
        metrics=metrics,
        monthly_sales_labels=monthly_sales['labels'],
        monthly_sales_data=monthly_sales['data'],
        active_reservations_labels=active_reservations['labels'],
        active_reservations_data=active_reservations['data']
    )
