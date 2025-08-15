from cotizador.firebase import get_db
import uuid
from datetime import datetime

def get_all_campanas():
    """Fetches all campanas from the database."""
    db = get_db()
    docs = db.collection('campanas').order_by('fecha_inicio').stream()
    return [doc.to_dict() for doc in docs]

def create_campana(data):
    """
    Creates a new campana document.
    A basic 'data' dict should include 'nombre_campana', 'cotizacion_id', etc.
    """
    db = get_db()
    doc_id = str(uuid.uuid4())
    data['id'] = doc_id
    data['fecha_creacion'] = datetime.now()
    db.collection('campanas').document(doc_id).set(data)
    return data

def get_campana_by_id(campana_id):
    """Fetches a single campana by its ID."""
    db = get_db()
    doc = db.collection('campanas').document(campana_id).get()
    return doc.to_dict() if doc.exists else None

def update_campana(campana_id, data):
    """Updates an existing campana document."""
    db = get_db()
    db.collection('campanas').document(campana_id).update(data)

def delete_campana(campana_id):
    """Deletes a campana document."""
    db = get_db()
    db.collection('campanas').document(campana_id).delete()
