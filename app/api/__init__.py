from flask.blueprints import Blueprint

bp = Blueprint('api', __name__)

from app.api import messages, user, search, static
