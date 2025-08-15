from flask import Blueprint

bp = Blueprint('agencias', __name__, url_prefix='/agencias', template_folder='templates')

from . import routes
