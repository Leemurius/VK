from flask import jsonify, request
from flask_login import login_required, current_user

from app.api.errors import bad_request
from app.api import bp
from app.main.queue import QueueControl
from config import Config


@bp.route('/self/queue/add', methods=['POST'])
@login_required
def add_to_queue():
    data = request.get_json() or {}
    try:
        QueueControl.add_to_queue(current_user, data['lab_number'])
    except Exception as exception:
        return bad_request(exception.args[0])
    return jsonify(True)


@bp.route('/queue/get', methods=['GET'])
@login_required
def get_queue():
    try:
        return jsonify(QueueControl.get_queue_in_dict())
    except Exception as exception:
        return bad_request(str(exception))


@bp.route('/queue/edit/index', methods=['POST', 'GET'])
@login_required
def edit_index():
    try:
        if current_user.email not in Config.ADMINS:
            raise Exception("You are not admin")

        data = request.get_json() or {}
        QueueControl.edit_index(data['number_in_queue'], data['new_number'])
    except Exception as exception:
        return bad_request(str(exception))
    return jsonify(True)


@bp.route('/queue/edit/status', methods=['POST', 'GET'])
@login_required
def edit_status():
    try:
        if current_user.email not in Config.ADMINS:
            raise Exception("You are not admin")
        data = request.get_json() or {}
        print(data)
        QueueControl.edit_status(data['number_in_queue'], data['new_status'])
    except Exception as exception:
        return bad_request(str(exception))
    return jsonify(True)


@bp.route('/queue/delete/user', methods=['POST', 'GET'])
@login_required
def delete_user():
    try:
        if current_user.email not in Config.ADMINS:
            raise Exception("You are not admin")

        data = request.get_json() or {}
        QueueControl.delete_user(data['number_in_queue'])
    except Exception as exception:
        return bad_request(str(exception))
    return jsonify(True)


@bp.route('/queue/self/get/status', methods=['GET'])
@login_required
def get_status():
    try:
        return jsonify(QueueControl.get_status(current_user))
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


@bp.route('/queue/start', methods=['POST', 'GET'])
@login_required
def start_queue():
    try:
        if current_user.email not in Config.ADMINS:
            raise Exception("You are not admin")
        QueueControl.start_queue()
    except Exception as exception:
        return bad_request(str(exception))
    return jsonify(True)


@bp.route('/queue/next', methods=['GET'])
@login_required
def get_next():
    try:
        return jsonify(QueueControl.get_next_user().username)
    except Exception as exception:
        return bad_request(str(exception))
