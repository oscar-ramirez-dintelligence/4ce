from flask import Blueprint

bp = Blueprint('soportes', __name__, url_prefix='/soportes')

from . import routes
