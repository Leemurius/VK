from flask import jsonify, request
from flask_login import login_required, current_user

from app.models import User, Room
from app.api import bp


@bp.route('/self/user_id', methods=['GET'])
@login_required
def get_self_id():
    return jsonify(current_user.id)


@bp.route('/self/user_photo', methods=['GET'])
@login_required
def get_self_photo():
    return jsonify(current_user.photo)


@bp.route('/profile_id/<string:nick>', methods=['GET'])
def get_id(nick):
    user = User.query.filter_by(nick=nick).first_or_404()
    return jsonify(user.id)


@bp.route('/messages', methods=['POST'])
@login_required
def add_message():
    data = request.get_json() or {}
    try:
        current_user.send_message(
            recipient_room=Room.query.get_or_404(data['room_id']),
            text=data['message']
        )
    except Exception:
        return jsonify(False)
    return jsonify(True)


@bp.route('/messages/example/<int:id>', methods=['GET'])
def example(id):
    return jsonify(User.query.get(id).to_dict())
