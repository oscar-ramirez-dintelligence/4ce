from cotizador.db import get_db
import uuid
import datetime

def get_all_cotizaciones(filters=None):
    """
    Fetches all cotizaciones, applying optional filters.
    """
    db = get_db()
    query = db.collection('cotizaciones')

    if filters:
        # Note: Firestore is limited in its querying capabilities.
        # For complex queries (e.g., text search, multiple inequality filters),
        # a search service like Algolia or Elasticsearch is recommended.
        # This implementation uses simple '==' equality checks.
        if filters.get('estado'):
            query = query.where('estado', '==', filters['estado'])
        if filters.get('anunciante'):
            query = query.where('anunciante', '==', filters['anunciante'])
        if filters.get('agencia'):
            query = query.where('agencia', '==', filters['agencia'])
        if filters.get('ejecutivo'):
            query = query.where('ejecutivo', '==', filters['ejecutivo'])

    # Order by a field for consistent results
    query = query.order_by('ultima_actualizacion', direction='DESCENDING')

    docs = query.stream()
    return [doc.to_dict() for doc in docs]

def create_cotizacion(data):
    """Creates a new cotizacion document."""
    db = get_db()
    doc_id = str(uuid.uuid4())
    data['id'] = doc_id
    data['ultima_actualizacion'] = datetime.datetime.now(datetime.timezone.utc)
    # Set a default status
    if 'estado' not in data:
        data['estado'] = 'Activa'

    db.collection('cotizaciones').document(doc_id).set(data)
    return data

def get_cotizacion_by_id(cotizacion_id):
    """Fetches a single cotizacion by its ID."""
    db = get_db()
    doc_ref = db.collection('cotizaciones').document(cotizacion_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

def update_cotizacion(cotizacion_id, data):
    """Updates an existing cotizacion document."""
    db = get_db()
    data['ultima_actualizacion'] = datetime.datetime.now(datetime.timezone.utc)
    db.collection('cotizaciones').document(cotizacion_id).update(data)
