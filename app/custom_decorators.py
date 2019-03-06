from functools import wraps
from flask_login import current_user
from flask import flash, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            flash({'head': u'Error!', 'msg': u'You cant visit this page!'}, 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
