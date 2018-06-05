"""
This file handles the Views for the user management system. 
"""

from flask import render_template, flash, redirect, url_for, \
        request, jsonify, session, send_from_directory
from app import app, db
from forms import RegistrationForm, EditProfileForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from app.decorator import requires_access_level
from pprint import pprint
import os 
from app.manage import bp

@bp.route('/')
def index():
    """Redirects to user management page."""

    return redirect(url_for('manage.users'))

@bp.route('/users', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def users():
    """Creates user management page."""

    sort = request.args.get('sort', 'username')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = UserTable(User.get_sorted_by(sort, reverse), 
            sort_by=sort, 
            sort_reverse=reverse)
    # table = UserTable(User.query.all())
    
    return render_template('manage/users.html', title='User\'s table', table=table)

@bp.route('/users/delete-<username>', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def deleteUser(username):
    """Deletes user if not current user
    
    Args:
        username (obj): Username object to delete
    """

    if str(username) in str(current_user):
        flash('You cannot delete your own account!', 'warning')
        return redirect(url_for('manage.users'))
    user = User.query.filter_by(username=username).first()
    # TODO Add Logging: User Deletion
    db.session.delete(user)
    db.session.commit()
    flash('User deleted!', 'success')

    return redirect(url_for('manage.users'))

@bp.route('/users/edit-<username>', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def editUser(username):
    """Allows an admin user the ability to add other users the system."""

    flash('Editing current user: ' + str(username), 'info')
    user = User.query.filter_by(username=username).first()
    form = EditProfileForm(obj=user)

    # TODO Add validation for CHANGED fields only
    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        db.session.commit()
        flash('User changed.', 'success')
        return redirect(url_for('manage.users'))

    return render_template('manage/edit.html', title='Edit - <username>', form=form)

@bp.route('/users/edit-<username>/reset-password', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def resetPassword(username):
    """Allows admin user to reset password of given user."""
    
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        user.set_password(form.password.data)
        db.session.commit()

    return render_template('manage/reset-password.html', title='Reset Password', form=form)

@bp.route('/register', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def register():
    """Allows an admin user the ability to add other users the system."""

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, \
                access=form.access.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered.', 'success')
        return redirect(url_for('manage.users'))

    return render_template('manage/register.html', title='Register', form=form)

