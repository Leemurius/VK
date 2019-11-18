from flask import jsonify, request
from flask_login import login_required, current_user

from app.api.errors import bad_request
from app.models import Room
from app.api import bp
from config import Constants


@bp.route('/messages', methods=['POST'])
@login_required
def add_message():
    data = request.get_json() or {}

    required_fields = ('room_id', 'message')
    if not all(field in data for field in required_fields):
        return bad_request('Must include ' + str(required_fields) + ' fields!')

    try:
        # TODO: separate function for validation
        if data['message'].strip() == '':  # Empty message
            return jsonify(False)

        if len(data['message']) > Constants.MAX_MESSAGE_LENGTH:  # Check length
            return jsonify(False)

        current_user.send_message(
            recipient_room=Room.query.get_or_404(data['room_id']),
            text=data['message']
        )
    except Exception as exception:
        return jsonify(False)
    return jsonify(True)
