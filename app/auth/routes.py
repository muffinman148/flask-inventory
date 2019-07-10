"""
This file handles the Views for the authentication system. 
"""

from flask import render_template, flash, redirect, url_for, \
        request, jsonify, session, send_from_directory
from werkzeug.urls import url_parse
from app import db
from app.auth.forms import LoginForm 
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.decorator import requires_access_level
import os 
from app.auth import bp

@bp.route('/login', methods=['GET','POST'])
def login():
    """Returns the login page. This page authenticates users."""

    if current_user.is_authenticated: # Redirects logged in users
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit(): # Checks form submission syntax validity
        user = User.query.filter_by(username=form.username.data).first()

        # Checks if username field is empty or password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))

        # User logged in successfully
        login_user(user, remember=form.remember_me.data)

        # Logs User into original inputted URL
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    """Logs user out. Redirects to login page."""

    # Clears old session variables
    session.pop('item', None)
    session.pop('mode', None)

    logout_user()

    return redirect(url_for('auth.login'))
