from flask import render_template, request, abort
from flask_login import current_user, login_required

from app.main import bp


@bp.route('/my_profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('main/profile.html', current_user=current_user)


@bp.route('/messages', methods=['GET'])
@login_required
def chat():
    recipient = request.args.get('sel', type=str)

    if recipient is None:
        abort(404)

    # if sel = 'c213'
    if not recipient.isdigit():
        # TODO: CHAT
        pass

    return render_template('main/chat.html', current_user=current_user)


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template('main/search.html', current_user=current_user)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update_status()
