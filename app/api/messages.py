from flask import jsonify, request
from flask_login import login_required, current_user

from app.api.errors import bad_request
from app.models import Dialog, User
from app.api import bp
from app.utils.validator import MessageValidator


@bp.route('/message/send/dialog', methods=['POST'])
@login_required
def add_message():
    data = request.get_json() or {}

    try:
        MessageValidator().validate({'recipient_id': int, 'message': str}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    current_user.send_message(
        room=Dialog.get_or_create(
            current_user,
            User.query.get_or_404(data['recipient_id'])
        ),
        text=data['message']
    )
    return jsonify(True)
