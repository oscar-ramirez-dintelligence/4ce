from cotizador.firebase import get_db

def get_all_tipos_cliente():
    """
    Fetches all client types from the Firestore database, ordered by name.
    """
    db = get_db()
    if not db:
        return []

    try:
        tipos_ref = db.collection('tipos_cliente').order_by('nombre').stream()
        return [tipo.to_dict() for tipo in tipos_ref]
    except Exception as e:
        print(f"An error occurred while fetching client types: {e}")
        return []

def get_tipo_cliente_by_id(tipo_id):
    """
    Fetches a single client type by its ID.
    """
    db = get_db()
    if not db:
        return None
    try:
        doc_ref = db.collection('tipos_cliente').document(tipo_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        print(f"An error occurred while fetching client type {tipo_id}: {e}")
        return None
