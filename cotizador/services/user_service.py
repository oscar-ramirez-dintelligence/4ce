import datetime
from cotizador.firebase import get_db, get_auth

def create_user(email, password, full_name, role):
    """
    Creates a new user in Firebase Authentication and stores their profile
    in the 'usuarios' collection in Firestore.
    """
    auth = get_auth()
    db = get_db()

    try:
        # Step 1: Create the user in Firebase Authentication
        user_record = auth.create_user(
            email=email,
            password=password,
            display_name=full_name,
            email_verified=False # Or True, depending on your flow
        )

        print(f"Successfully created new auth user: {user_record.uid}")

        # Step 2: Create the user profile document in Firestore
        user_data = {
            'uid': user_record.uid,
            'nombre_completo': full_name,
            'email': email,
            'rol': role,
            'fecha_creacion': datetime.datetime.now(datetime.timezone.utc),
            'fecha_ultimo_ingreso': None
        }

        db.collection('usuarios').document(user_record.uid).set(user_data)
        print(f"Successfully created user profile in Firestore for {user_record.uid}")

        return user_data

    except Exception as e:
        # In a production app, you'd want more robust error handling,
        # potentially including a compensating transaction to delete the
        # auth user if the Firestore write fails.
        print(f"An error occurred during user creation: {e}")
        return None

def get_all_users():
    """
    Retrieves all user profiles from the 'usuarios' Firestore collection.
    """
    db = get_db()
    if not db:
        print("Error: Database connection not available.")
        return []

    try:
        users_ref = db.collection('usuarios').order_by('nombre_completo').stream()
        return [user.to_dict() for user in users_ref]
    except Exception as e:
        print(f"An error occurred while fetching all users: {e}")
        return []

def get_user_by_uid(uid):
    """
    Retrieves a single user profile from Firestore by their UID.
    """
    db = get_db()
    if not db:
        return None
    try:
        doc_ref = db.collection('usuarios').document(uid)
        user = doc_ref.get()
        return user.to_dict() if user.exists else None
    except Exception as e:
        print(f"An error occurred while fetching user {uid}: {e}")
        return None

# Note: For a full implementation, you would also add functions here for:
# - update_user(uid, data): Updates a user's profile in Firestore and Firebase Auth.
# - delete_user(uid): Deletes a user from Firebase Auth and their profile from Firestore.
# - get_user_by_email(email): Retrieves a user by their email address.
