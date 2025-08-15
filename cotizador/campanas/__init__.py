from flask import Blueprint

bp = Blueprint('campanas', __name__, url_prefix='/campanas', template_folder='templates')

from . import routes
