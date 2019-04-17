from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app.settings import bp
from app.settings.forms import (
    ProfSettingsForm,
    SecSettingsForm,
    AboutSettingsForm,
)
from app.main.forms import SearchForm


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    base_form = SearchForm()
    rooms = base_form.get_founding_room(current_user)  # validate inside

    form = ProfSettingsForm(
        name=current_user.name,
        surname=current_user.surname,
        nick=current_user.nick,
        age=current_user.age,
        email=current_user.email,
        address=current_user.address
    )

    if form.validate_on_submit():
        current_user.set_profile_form(form)
        return redirect(url_for('settings.profile'))

    return render_template(
        'settings/profile.html',
        base_form=base_form,  # for base.html
        current_user=current_user,  # for base.html
        rooms=rooms,  # for base.html
        form=form
    )


@bp.route('/security', methods=['GET', 'POST'])
@login_required
def security():
    base_form = SearchForm()
    form = SecSettingsForm()
    rooms = base_form.get_founding_room(current_user)  # validate inside

    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        return redirect(url_for('settings.security'))

    return render_template(
        'settings/security.html',
        base_form=base_form,  # for base.html
        current_user=current_user,  # for base.html
        rooms=rooms,  # for base.html
        form=form
    )


@bp.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    base_form = SearchForm()
    form = AboutSettingsForm(about_me=current_user.about_me)
    rooms = base_form.get_founding_room(current_user)  # validate inside

    if form.validate_on_submit():
        current_user.set_about_form(form)
        return redirect(url_for('settings.about'))

    return render_template(
        'settings/about.html',
        base_form=base_form,  # for base.html
        current_user=current_user,  # for base.html
        rooms=rooms,  # for base.html
        form=form
    )
