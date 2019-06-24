from flask import jsonify
from flask_login import current_user

from app.api import bp
from app.models import Room, User


@bp.route('/rooms/<int:profile_id>', methods=['GET'])
def get_room_or_create(profile_id):
    profile_user = User.query.get_or_404(profile_id)
    room_id = Room.get_or_create_room(current_user, profile_user)
    return jsonify(room_id)