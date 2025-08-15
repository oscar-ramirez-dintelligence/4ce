from cotizador.db import get_db
import uuid

def get_paginated_soportes(start_at_doc=None, filters=None):
    """
    Fetches a paginated and filtered list of soportes.
    `filters` is a dict with potential keys like 'nombre', 'codigo', 'tipo', etc.
    """
    db = get_db()
    if not db:
        return [], None

    query = db.collection('soportes')

    # Apply filters if any
    if filters:
        if filters.get('nombre_soporte'):
            # Firestore does not support partial string matches (LIKE queries).
            # A common workaround is to use a third-party search service like Algolia or Elasticsearch,
            # or to perform range-based queries on the string field.
            # For now, we'll do a simple equality check.
            query = query.where('nombre_soporte', '==', filters['nombre_soporte'])
        if filters.get('codigo_soporte'):
            query = query.where('codigo_soporte', '==', filters['codigo_soporte'])
        if filters.get('tipo_soporte'):
            query = query.where('tipo_soporte', '==', filters['tipo_soporte'])
        # Add other filters as needed

    # Always order by a field for consistent pagination
    query = query.order_by('codigo_soporte')

    if start_at_doc:
        query = query.start_after(start_at_doc)

    soportes_docs = list(query.limit(10).stream())

    next_page_cursor = None
    if len(soportes_docs) == 10:
        next_page_cursor = soportes_docs[-1]

    soportes = [doc.to_dict() for doc in soportes_docs]
    return soportes, next_page_cursor

def create_soporte(data):
    """Creates a new soporte document."""
    db = get_db()
    doc_id = str(uuid.uuid4())
    data['id'] = doc_id
    db.collection('soportes').document(doc_id).set(data)
    return data

def get_soporte_by_id(soporte_id):
    """Fetches a single soporte by its ID."""
    db = get_db()
    doc_ref = db.collection('soportes').document(soporte_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

def update_soporte(soporte_id, data):
    """Updates an existing soporte document."""
    db = get_db()
    db.collection('soportes').document(soporte_id).update(data)

def delete_soporte(soporte_id):
    """Deletes a soporte document."""
    db = get_db()
    db.collection('soportes').document(soporte_id).delete()
