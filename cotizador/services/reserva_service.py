from cotizador.db import get_db
import uuid
from datetime import datetime

def get_all_reservas():
    """Fetches all reservas from the database."""
    db = get_db()
    docs = db.collection('reservas').order_by('fecha_inicio').stream()
    return [doc.to_dict() for doc in docs]

def create_reserva(data):
    """
    Creates a new reserva document.
    A basic 'data' dict should include 'soporte_id', 'fecha_inicio', 'fecha_fin'.
    """
    db = get_db()
    doc_id = str(uuid.uuid4())
    data['id'] = doc_id
    data['fecha_creacion'] = datetime.now()
    db.collection('reservas').document(doc_id).set(data)
    return data

def get_reserva_by_id(reserva_id):
    """Fetches a single reserva by its ID."""
    db = get_db()
    doc = db.collection('reservas').document(reserva_id).get()
    return doc.to_dict() if doc.exists else None

def update_reserva(reserva_id, data):
    """Updates an existing reserva document."""
    db = get_db()
    db.collection('reservas').document(reserva_id).update(data)

def delete_reserva(reserva_id):
    """Deletes a reserva document."""
    db = get_db()
    db.collection('reservas').document(reserva_id).delete()
