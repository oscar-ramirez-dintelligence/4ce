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
            # The client uses the GOOGLE_APPLICATION_CREDENTIALS env var automatically
            g.db = google.cloud.firestore.Client()
            print("Firestore client initialized successfully for this context.")
        except Exception as e:
            print(f"Error initializing Firestore client: {e}")
            # Return None or handle the error as appropriate for your app
            g.db = None
    return g.db

def close_db(e=None):
    """
    Closes the database connection. This can be registered with the
    application context to be called automatically on teardown.
    """
    db = g.pop('db', None)
    # Firestore client doesn't have an explicit close() method that's necessary
    # for standard request/response cycles. The library manages connections.
    # This function is here for pattern consistency.
    if db is not None:
        # No explicit close needed.
        pass

def init_app(app):
    """
    Registers database functions with the Flask app. This is called from
    the application factory.
    """
    app.teardown_appcontext(close_db)
