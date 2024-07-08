""" routes for users """
import logging
from datetime import datetime
from flask_mail import Message
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from TaskManager import db, bcrypt, mail
from TaskManager.users.forms import (ResetPasswordForm, RequestResetForm,
                               RegistrationUserForm, LoginForm, UpdateAccountForm)
from TaskManager.models import User


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    """Route to handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationUserForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    """Route to handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)

            current_user.last_login = datetime.utcnow()
            db.session.add(current_user)
            db.session.commit()

            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    """Route to handle user logout."""
    current_user.last_login = datetime.utcnow()
    db.session.add(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Route to handle account updates."""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        current_user.last_login = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        if current_user.is_authenticated:
            form.username.data = current_user.username
            form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    print(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('main.login'))

    return render_template('token_reset.html', title='Reset Password', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('password Reset Request', sender=('TaskManager', 'noreply@demo.com'), recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
'''
    try:
        mail.send(msg)
        logging.info(f"Password reset email sent to {user.email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
