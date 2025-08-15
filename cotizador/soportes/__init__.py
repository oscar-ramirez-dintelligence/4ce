from flask import Blueprint

bp = Blueprint('soportes', __name__, url_prefix='/soportes', template_folder='templates')

from . import routes
