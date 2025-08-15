import os
from flask import Flask

def create_app(test_config=None):
    """
    The application factory. This function is responsible for creating and
    configuring the Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)

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

    from . import firebase
    firebase.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import main
    app.register_blueprint(main.bp)

    from . import soportes
    app.register_blueprint(soportes.bp)

    from . import cotizaciones
    app.register_blueprint(cotizaciones.bp)

    from . import agencias
    app.register_blueprint(agencias.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)

    # The main dashboard is now at /dashboard, but we can keep the root
    # pointing to the simple main page for now. The nav bar will point to the dashboard.
    app.add_url_rule('/', endpoint='index')

    return app
