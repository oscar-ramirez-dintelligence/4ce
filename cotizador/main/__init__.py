from flask import Blueprint

bp = Blueprint('main', __name__)

# Import routes at the end to avoid circular dependencies
from . import routes
