from flask import Blueprint

bp = Blueprint('reservas', __name__, url_prefix='/reservas', template_folder='templates')

from . import routes
