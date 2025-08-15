import datetime
import uuid
from cotizador.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(email, password, full_name, role):
    """
    Creates a new user with a hashed password in the 'usuarios' collection.
    """
    db = get_db()

    # Check if user already exists
    existing_user = get_user_by_email(email)
    if existing_user:
        raise ValueError(f"User with email {email} already exists.")

    user_data = {
        'uid': str(uuid.uuid4()),
        'nombre_completo': full_name,
        'email': email,
        'password_hash': generate_password_hash(password),
        'rol': role,
        'fecha_creacion': datetime.datetime.now(datetime.timezone.utc),
        'fecha_ultimo_ingreso': None
    }

    db.collection('usuarios').document(user_data['uid']).set(user_data)
    return user_data

def check_credentials(email, password):
    """
    Verifies a user's credentials. Returns the user dict if valid, otherwise None.
    """
    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        # Update last login timestamp
        db = get_db()
        db.collection('usuarios').document(user['uid']).update({
            'fecha_ultimo_ingreso': datetime.datetime.now(datetime.timezone.utc)
        })
        return user
    return None

def get_user_by_email(email):
    """
    Retrieves a single user profile from Firestore by their email address.
    """
    db = get_db()
    if not db:
        return None

    users_ref = db.collection('usuarios').where('email', '==', email).limit(1)
    docs = list(users_ref.stream())

    if docs:
        return docs[0].to_dict()
    return None

def get_all_users():
    """
    Retrieves all user profiles from the 'usuarios' Firestore collection.
    """
    db = get_db()
    if not db:
        return []

    users_ref = db.collection('usuarios').order_by('nombre_completo').stream()
    return [user.to_dict() for user in users_ref]

def get_user_by_uid(uid):
    """
    Retrieves a single user profile from Firestore by their UID.
    """
    db = get_db()
    if not db:
        return None

    doc_ref = db.collection('usuarios').document(uid)
    user = doc_ref.get()
    return user.to_dict() if user.exists else None
