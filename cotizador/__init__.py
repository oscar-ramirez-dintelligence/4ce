import os
from flask import Flask

def create_app(test_config=None):
    """
    The application factory.
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

    # Register Blueprints
    from . import auth, admin, main, soportes, cotizaciones, agencias, dashboard, reportes, reservas, campanas
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(soportes.bp)
    app.register_blueprint(cotizaciones.bp)
    app.register_blueprint(agencias.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(reportes.bp)
    app.register_blueprint(reservas.bp)
    app.register_blueprint(campanas.bp)

    app.add_url_rule('/', endpoint='index')

    return app
