from flask import jsonify, request
from flask_login import login_required, current_user

from app.models import Room
from app.api import bp


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
