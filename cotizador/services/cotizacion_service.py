from cotizador.db import get_db

def get_all_cotizaciones():
    """
    Fetches all cotizaciones from the database, ordered by title.
    """
    db = get_db()
    if not db:
        return []
    try:
        cotizaciones_ref = db.collection('cotizaciones').order_by('titulo').stream()
        return [c.to_dict() for c in cotizaciones_ref]
    except Exception as e:
        print(f"An error occurred while fetching all cotizaciones: {e}")
        return []

def get_cotizacion_by_id(cotizacion_id):
    """
    Fetches a single cotizacion by its document ID.
    """
    db = get_db()
    if not db:
        return None
    try:
        doc_ref = db.collection('cotizaciones').document(cotizacion_id)
        cotizacion = doc_ref.get()
        return cotizacion.to_dict() if cotizacion.exists else None
    except Exception as e:
        print(f"An error occurred while fetching cotizacion {cotizacion_id}: {e}")
        return None

def create_cotizacion(data):
    """
    Creates a new cotizacion document in the database.
    """
    db = get_db()
    if not db:
        return None
    try:
        # In a real-world scenario, you could add more business logic here, such as:
        # - Validating that the selected soportes and tipo_cliente exist.
        # - Calculating a total price based on the selected items and discounts.
        # - Storing denormalized data for performance (e.g., a copy of the soporte name).

        collection_ref = db.collection('cotizaciones')
        doc_ref = collection_ref.document()
        data['id'] = doc_ref.id
        doc_ref.set(data)
        return data
    except Exception as e:
        print(f"An error occurred while creating cotizacion: {e}")
        return None
