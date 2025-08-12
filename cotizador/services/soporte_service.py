from cotizador.db import get_db

SOPORTES_PER_PAGE = 9

def get_paginated_soportes(start_at_doc_id=None):
    """
    Fetches a paginated list of soportes from the database.
    Returns a tuple of (soportes_list, next_page_cursor).
    """
    db = get_db()
    if not db:
        return [], None

    try:
        soportes_ref = db.collection('soportes')
        query = soportes_ref.order_by('codigo')

        if start_at_doc_id:
            start_at_doc = soportes_ref.document(start_at_doc_id).get()
            if start_at_doc.exists:
                query = query.start_after(start_at_doc)

        soportes_docs = list(query.limit(SOPORTES_PER_PAGE).stream())
        soportes = [doc.to_dict() for doc in soportes_docs]

        next_page_cursor = None
        if len(soportes_docs) == SOPORTES_PER_PAGE:
            next_page_cursor = soportes_docs[-1].id

        return soportes, next_page_cursor
    except Exception as e:
        print(f"An error occurred while fetching paginated soportes: {e}")
        return [], None

def get_all_soportes():
    """
    Fetches all soportes from the database, ordered by name.
    """
    db = get_db()
    if not db:
        return []
    try:
        soportes_ref = db.collection('soportes').order_by('nombre').stream()
        return [s.to_dict() for s in soportes_ref]
    except Exception as e:
        print(f"An error occurred while fetching all soportes: {e}")
        return []

def get_soporte_by_id(soporte_id):
    """
    Fetches a single soporte by its document ID.
    """
    db = get_db()
    if not db:
        return None
    try:
        doc_ref = db.collection('soportes').document(soporte_id)
        soporte = doc_ref.get()
        return soporte.to_dict() if soporte.exists else None
    except Exception as e:
        print(f"An error occurred while fetching soporte {soporte_id}: {e}")
        return None

def create_soporte(data):
    """
    Creates a new soporte document in the database.
    """
    db = get_db()
    if not db:
        return None
    try:
        collection_ref = db.collection('soportes')
        doc_ref = collection_ref.document()
        data['id'] = doc_ref.id
        doc_ref.set(data)
        return data
    except Exception as e:
        print(f"An error occurred while creating a soporte: {e}")
        return None

def update_soporte(soporte_id, data):
    """
    Updates an existing soporte document.
    """
    db = get_db()
    if not db:
        return None
    try:
        doc_ref = db.collection('soportes').document(soporte_id)
        if not doc_ref.get().exists:
            return None
        doc_ref.update(data)
        updated_doc = doc_ref.get()
        return updated_doc.to_dict()
    except Exception as e:
        print(f"An error occurred while updating soporte {soporte_id}: {e}")
        return None

def delete_soporte(soporte_id):
    """
    Deletes a soporte document. Returns True on success, False on failure.
    """
    db = get_db()
    if not db:
        return False
    try:
        doc_ref = db.collection('soportes').document(soporte_id)
        if not doc_ref.get().exists:
            print(f"Attempted to delete non-existent soporte: {soporte_id}")
            return False
        doc_ref.delete()
        return True
    except Exception as e:
        print(f"An error occurred while deleting soporte {soporte_id}: {e}")
        return False
