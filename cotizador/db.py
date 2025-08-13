import os
import google.cloud.firestore
from flask import g

def get_db():
    """
    Connects to the Firestore database. If the connection is not already
    established for the current application context, it creates one.
    """
    if 'db' not in g:
        try:
            # Explicitly pass the project ID from the environment variable.
            # The library can often infer this, but being explicit is more robust.
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

            g.db = google.cloud.firestore.Client(project=project_id)
            print(f"Firestore client initialized for project: {project_id}")
        except Exception as e:
            print(f"Error initializing Firestore client: {e}")
            g.db = None
    return g.db

def close_db(e=None):
    """
    Closes the database connection on application context teardown.
    """
    db = g.pop('db', None)
    # The Firestore client library manages connections automatically,
    # so there's no explicit close() method to call.
    if db is not None:
        pass

def init_app(app):
    """
    Registers database functions with the Flask app.
    """
    app.teardown_appcontext(close_db)
