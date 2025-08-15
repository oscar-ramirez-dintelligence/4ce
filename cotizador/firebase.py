import os
import firebase_admin
from firebase_admin import credentials, auth
from google.cloud import firestore
from flask import g

def init_firebase():
    """
    Initializes the Firebase Admin SDK.
    It uses a service account key file if the path is provided in the env,
    otherwise it falls back to Application Default Credentials (ADC),
    which is ideal for Google Cloud environments like Cloud Run.
    """
    if not firebase_admin._apps:
        cred_path = os.getenv('FIREBASE_ADMIN_SDK_CONFIG')
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")

        cred_options = {'project_id': project_id}

        if cred_path:
            cred = credentials.Certificate(cred_path)
        else:
            # Use Application Default Credentials
            cred = credentials.ApplicationDefault()

        firebase_admin.initialize_app(cred, cred_options)
        print("Firebase Admin SDK initialized successfully.")

def get_db():
    """
    Returns a Firestore client instance, reusing it if it exists
    on the application context.
    """
    if 'db' not in g:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        g.db = firestore.Client(project=project_id)
    return g.db

def get_auth():
    """
    Returns the Firebase Auth module client.
    """
    return auth

def init_app(app):
    """
    Initializes Firebase and sets up context processors for the Flask app.
    """
    init_firebase()

    @app.before_request
    def before_request():
        # Make the db client available on every request via g
        g.db = get_db()

    @app.teardown_appcontext
    def teardown_db(exception):
        # The library handles connection pooling, so no explicit close is needed.
        db = g.pop('db', None)
        if db is not None:
            pass
