from cotizador.db import get_db

def get_all_tipos_cliente():
    """
    Fetches all client types from the Firestore database, ordered by name.

    Returns:
        list: A list of dictionaries, where each dictionary represents a client type.
              Returns an empty list if the database is unavailable or an error occurs.
    """
    db = get_db()
    if not db:
        print("Error: Database connection not available.")
        return []

    try:
        tipos_ref = db.collection('tipos_cliente').order_by('nombre').stream()
        tipos = [tipo.to_dict() for tipo in tipos_ref]
        return tipos
    except Exception as e:
        print(f"An error occurred while fetching client types: {e}")
        return []
