import re

from flask_login import login_required
from flask import current_app, request, jsonify

from api.errors import bad_request
from app.api import bp
from app.utils.validator import ContentValidator, FilenameValidator


@bp.route('/html/get', methods=['POST'])
@login_required
def get_html_block():
    data = request.get_json() or {}

    # Validation
    try:
        ContentValidator().validate(('blockname', 'filename'), data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    return jsonify(get_block_from_html(data['blockname'], data['filename']))


@bp.route('/js/list/get', methods=['POST'])
@login_required
def get_list_of_js_from_html():
    data = request.get_json() or {}

    # Validation
    try:
        FilenameValidator().validate(('filename', ), data)
    except ValueError as exception:
        return bad_request(exception.args[0])

    content = get_block_from_html('js_files', data['filename'])
    return jsonify(get_list_of_js_from_block(content))


def get_block_from_html(blockname, filename):
    block = ''
    can_write = False

    with open(current_app.root_path + filename) as file:
        for line in file:
            # Crutch that deletes Jinja's things like "{{ some() }}" and comments from html
            if re.findall('.*\{\{.+\}\}.*', line) or re.findall('.*\{#.+#\}.*', line):
                continue

            if can_write is True and line in ('{% endblock %}\n', '{% endblock %}'):
                can_write = False

            if can_write:
                block += line

            if line == '{{% block {} %}}\n'.format(blockname):
                can_write = True

    return block


def get_list_of_js_from_block(content):
    js_list = []

    # Crutch that parses LINK from <script src="LINK"></script>.
    for line in content.split('\n'):
        splitted = line.split('\"')
        if len(splitted) > 1:
            js_list.append(splitted[1])

    return js_list
