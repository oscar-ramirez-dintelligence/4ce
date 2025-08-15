from cotizador.firebase import get_db
from datetime import datetime

def generate_report(report_type, start_date_str, end_date_str):
    """
    Generates data for a specified report type and date range.
    """
    if report_type == 'listado_cotizaciones':
        return generate_cotizaciones_report(start_date_str, end_date_str)
    # Add other report types here
    # elif report_type == 'ventas_por_ejecutivo':
    #     return generate_ventas_report(start_date, end_date)
    else:
        return None, None

def generate_cotizaciones_report(start_date_str, end_date_str):
    """
    Generates a report of all quotations within a given date range.
    """
    db = get_db()
    query = db.collection('cotizaciones')

    # Apply date filters
    if start_date_str:
        start_date = datetime.fromisoformat(start_date_str)
        query = query.where('ultima_actualizacion', '>=', start_date)
    if end_date_str:
        # For a '<=' query, we might need a second inequality which requires a composite index in Firestore.
        # For simplicity, we will handle this in Python for now.
        end_date = datetime.fromisoformat(end_date_str)
        # query = query.where('ultima_actualizacion', '<=', end_date) # This line would require an index

    # Order by date
    query = query.order_by('ultima_actualizacion', direction='DESCENDING')

    docs = query.stream()

    # Filter by end_date in Python if necessary
    report_data = [doc.to_dict() for doc in docs]
    if end_date_str:
        end_date = datetime.fromisoformat(end_date_str).replace(tzinfo=datetime.timezone.utc)
        report_data = [
            row for row in report_data
            if row.get('ultima_actualizacion') and row['ultima_actualizacion'] <= end_date
        ]

    headers = [
        "ID", "Título", "Anunciante", "Agencia", "Ejecutivo",
        "Estado", "Presupuesto Estimado", "Última Actualización"
    ]

    # Map Firestore data to the headers
    rows = []
    for item in report_data:
        rows.append({
            "ID": item.get('id', ''),
            "Título": item.get('titulo', ''),
            "Anunciante": item.get('anunciante', ''),
            "Agencia": item.get('agencia', ''),
            "Ejecutivo": item.get('ejecutivo', ''),
            "Estado": item.get('estado', ''),
            "Presupuesto Estimado": item.get('presupuesto_estimado', 0),
            "Última Actualización": item.get('ultima_actualizacion', '').strftime('%Y-%m-%d') if item.get('ultima_actualizacion') else ''
        })

    return headers, rows
