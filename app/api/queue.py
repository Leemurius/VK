from flask import jsonify, request
from flask_login import login_required, current_user

from app.api.errors import bad_request
from app.api import bp
from app.main.queue import QueueControl


@bp.route('/self/queue/add', methods=['POST'])
@login_required
def add_to_queue():
    data = request.get_json() or {}
    try:
        QueueControl.add_to_queue(current_user, data['lab_number'])
    except Exception as exception:
        return bad_request(str(exception))
    return jsonify(True)


@bp.route('/queue/get', methods=['GET'])
@login_required
def get_queue():
    try:
        return jsonify(QueueControl.get_queue())
    except Exception as exception:
        return bad_request(str(exception))


@bp.route('/queue/change/status', methods=['POST'])
@login_required
def change_queue_status():
    data = request.get_json() or {}
    try:
        QueueControl.change_status(current_user, data['status'])
    except Exception as exception:
        return bad_request(str(exception))
    return jsonify(True)


@bp.route('/queue/start', methods=['POST'])
@login_required
def start_queue():
    try:
        return jsonify(QueueControl.start_queue())
    except Exception as exception:
        return bad_request(str(exception))


@bp.route('/queue/terminate', methods=['POST'])
@login_required
def terminate_queue():
    try:
        return jsonify(QueueControl.terminate_queue())
    except Exception as exception:
        return bad_request(str(exception))


@bp.route('/queue/next', methods=['POST'])
@login_required
def get_next():
    try:
        return jsonify(QueueControl.get_next())
    except Exception as exception:
        return bad_request(str(exception))
