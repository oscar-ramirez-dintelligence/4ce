import os
from flask import Flask

def create_app(test_config=None):
    """
    The application factory. This function is responsible for creating and
    configuring the Flask application instance.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # --- Configuration ---
    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'a-very-insecure-default-key'),
        # The GOOGLE_MAPS_API_KEY will be loaded directly via os.getenv in the route
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        # This can be used for production secrets not in .env
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- Initialize Extensions (Database) ---
    from . import db
    db.init_app(app)

    # --- Register Blueprints ---
    # Each blueprint corresponds to a feature/section of the app.

    from .main import routes as main_routes
    app.register_blueprint(main_routes.bp)

    from .soportes import routes as soportes_routes
    app.register_blueprint(soportes_routes.bp)

    from .cotizaciones import routes as cotizaciones_routes
    app.register_blueprint(cotizaciones_routes.bp)

    from .api import routes as api_routes
    app.register_blueprint(api_routes.bp)

    # Make the app aware of the index route if it's in a blueprint
    # This ensures url_for('index') works. 'main.index_page' is more specific.
    app.add_url_rule('/', endpoint='index')

    return app
