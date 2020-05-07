from flask import jsonify, request
from flask_login import current_user

from app.api import bp
from app.api.errors import bad_request
from app.models import User, Dialog
from app.utils.validator import Validator


@bp.route('/dialog/get/messages', methods=['POST'])
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
