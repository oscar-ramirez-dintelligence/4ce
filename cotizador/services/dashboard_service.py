from cotizador.db import get_db
from datetime import datetime

def get_dashboard_metrics():
    """
    Calculates the main metrics for the sales dashboard.
    NOTE: This is a placeholder implementation. Real-world calculations,
    especially for aggregations like sums and averages across many documents,
    can be inefficient in Firestore and might require different strategies
    (like using Cloud Functions to maintain aggregate counters).
    """
    db = get_db()

    # --- Metric 1: Active Quotes ---
    cotizaciones_ref = db.collection('cotizaciones').where('estado', '==', 'Activa')
    active_quotes_docs = list(cotizaciones_ref.stream())
    active_quotes_count = len(active_quotes_docs)
    active_quotes_amount = sum(doc.to_dict().get('presupuesto_estimado', 0) for doc in active_quotes_docs)

    # --- Metrics 2 & 3: Campaigns (Placeholder) ---
    # These require a 'campañas' collection which is not yet implemented.
    campaigns_exhibited_amount = 0
    campaigns_notified_amount = 0

    # --- Metric 4: Occupation (Placeholder) ---
    # This would require a complex calculation involving all soportes and their
    # reservations/campaigns over a period of time.
    occupation_percentage = 0.0

    return {
        "active_quotes_count": active_quotes_count,
        "active_quotes_amount": active_quotes_amount,
        "campaigns_exhibited_amount": campaigns_exhibited_amount,
        "campaigns_notified_amount": campaigns_notified_amount,
        "occupation_percentage": occupation_percentage,
    }

def get_monthly_sales_data():
    """
    Generates data for the monthly sales bar chart.
    NOTE: This is a placeholder. A real implementation would need to query
    a 'ventas' or 'campañas' collection and aggregate by month.
    """
    return {
        "labels": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"],
        "data": [12000, 19000, 3000, 5000, 2000, 30000]
    }

def get_active_reservations_data():
    """
    Generates data for the active reservations bar chart.
    NOTE: This is a placeholder. Requires a 'reservas' collection.
    """
    return {
        "labels": ["Julio", "Agosto", "Septiembre"],
        "data": [15, 25, 20]
    }
