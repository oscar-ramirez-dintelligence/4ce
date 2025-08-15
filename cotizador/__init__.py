import os
from flask import Flask

def create_app(test_config=None):
    """
    The application factory. This function is responsible for creating and
    configuring the Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- Initialize Firebase Admin SDK and Firestore ---
    from . import firebase
    firebase.init_app(app)

    # --- Register Blueprints ---
    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import main
    app.register_blueprint(main.bp)

    return app
