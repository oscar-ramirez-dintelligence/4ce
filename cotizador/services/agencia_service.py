from cotizador.firebase import get_db
import uuid

def get_all_agencias(filters=None):
    """
    Fetches all agencias, applying optional filters.
    """
    db = get_db()
    query = db.collection('agencias')

    if filters:
        if filters.get('nombre'):
            query = query.where('nombre', '>=', filters['nombre']).where('nombre', '<=', filters['nombre'] + u'\uf8ff')
        if filters.get('rfc'):
            query = query.where('rfc', '==', filters['rfc'])
        if filters.get('grupo'):
            query = query.grupowhere('grupo', '==', filters['grupo'])

    query = query.order_by('nombre')

    docs = query.stream()
    return [doc.to_dict() for doc in docs]

def create_agencia(data):
    """Creates a new agencia document."""
    db = get_db()
    doc_id = str(uuid.uuid4())
    data['id'] = doc_id
    db.collection('agencias').document(doc_id).set(data)
    return data

def get_agencia_by_id(agencia_id):
    """Fetches a single agencia by its ID."""
    db = get_db()
    doc_ref = db.collection('agencias').document(agencia_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

def update_agencia(agencia_id, data):
    """Updates an existing agencia document."""
    db = get_db()
    db.collection('agencias').document(agencia_id).update(data)

def delete_agencia(agencia_id):
    """Deletes an agencia document."""
    db = get_db()
    db.collection('agencias').document(agencia_id).delete()
