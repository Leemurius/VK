from flask import jsonify, request
from flask_login import login_required, current_user

from app.api import bp
from app.models import Dialog, User
from app.utils.validator import Validator, MessageValidator
from app.utils.errors import bad_request


@bp.route('/messages/send', methods=['POST'])
@login_required
def add_message():
    # TODO: CHAT

    data = request.get_json() or {}

    try:
        MessageValidator.validate({'recipient_id': int, 'message': str}, data)
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


@bp.route('/messages/getDialogHistory', methods=['POST'])
def get_dialog():
    data = request.get_json() or {}

    # Validation
    try:
        Validator.validate_required_fields({'profile_id': int}, data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    dialog = Dialog.get_object(
        current_user,
        User.query.get_or_404(data['profile_id'])
    )
    if dialog is None:
        return jsonify([])
    else:
        return jsonify(dialog.get_messages())
