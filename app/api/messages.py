from flask import jsonify, request
from flask_login import login_required, current_user

from app.api.errors import bad_request
from app.models import Room
from app.api import bp
from app.utils.validator import MessageValidator


@bp.route('/messages', methods=['POST'])
@login_required
def add_message():
    data = request.get_json() or {}

    try:
        MessageValidator().validate(('room_id', 'message'), data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    current_user.send_message(
        recipient_room=Room.query.get_or_404(data['room_id']),
        text=data['message']
    )
    return jsonify(True)
