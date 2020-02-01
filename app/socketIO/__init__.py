from flask import Blueprint

bp = Blueprint('socketIO', __name__)

from app.socketIO import user
