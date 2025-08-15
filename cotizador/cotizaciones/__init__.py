from flask import Blueprint

bp = Blueprint('cotizaciones', __name__, url_prefix='/cotizaciones', template_folder='templates')

from . import routes
