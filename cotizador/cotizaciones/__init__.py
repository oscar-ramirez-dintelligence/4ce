from flask import Blueprint

bp = Blueprint('cotizaciones', __name__, url_prefix='/cotizaciones')

from . import routes
