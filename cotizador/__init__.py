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
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- Initialize Extensions (Database) ---
    from . import db
    db.init_app(app)

    # --- Register Blueprints ---
    # Import the blueprint packages and register their 'bp' attribute.
    from . import main
    app.register_blueprint(main.bp)

    from . import soportes
    app.register_blueprint(soportes.bp)

    from . import cotizaciones
    app.register_blueprint(cotizaciones.bp)

    from . import api
    app.register_blueprint(api.bp)

    # Add a URL rule for the index endpoint to make url_for('index') work.
    # The endpoint name defaults to the function name, 'index_page'.
    app.add_url_rule('/', endpoint='index')

    return app
