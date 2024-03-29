from flask import redirect, url_for, flash, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from flask_babel import _

from .email import send_password_reset_email
from .forms import LoginForm, ResetPasswordForm, ResetPasswordRequestForm, RegistrationForm
from . import auth_bp
from app.models import User
from app import db


@auth_bp.route("/login/", methods=['POST', "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid credentials'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form, title=_("Sign In"))


@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/register/', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_("Congrats, you are registered!"))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title=_("Sign Up"))


@auth_bp.route('/reset_password_request/', methods=["POST", "GET"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_("An password resetting email has been sent to your email"))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form, title=_("Reset Password"))


@auth_bp.route("/reset_password/<token>", methods=["POST", "GET"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        user.set_password(password)
        db.session.commit()
        flash(_("Your password is successfully updated"))
        return redirect(url_for('auth.login'))
    return render_template("auth/reset_password.html", form=form, title=_("Reset Passwrod"))
