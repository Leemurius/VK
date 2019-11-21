from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app.settings import bp


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    rooms = current_user.rooms

    return render_template(
        'main/settings.html',
        current_user=current_user,  # for base.html
        rooms=rooms  # for base.html
    )