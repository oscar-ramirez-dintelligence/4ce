from flask import Blueprint

bp = Blueprint('reportes', __name__, url_prefix='/reportes', template_folder='templates')

from . import routes
