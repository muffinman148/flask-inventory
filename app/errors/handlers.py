"""
This file handles HTTP standard response codes.
"""

from flask import render_template, flash, redirect, url_for
from app import app, db
from app.errors import bp

@bp.app_errorhandler(401)
def page_not_found(e):
    """Redirects users without proper access to login page."""

    flash('Page not found.', 'warning')

    return redirect(url_for('auth.login'))

@bp.app_errorhandler(404)
def not_found_error(error):
    """Returns 404 error page."""

    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    """Returns 500 error page. Cancels uncommitted database changes."""

    db.session.rollback()

    return render_template('errors/500.html'), 500
