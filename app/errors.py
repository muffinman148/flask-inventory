"""
This file handles HTTP standard response codes.
"""

from flask import render_template
from app import app, db

@app.errorhandler(401)
def page_not_found(e):
    """Redirects users without proper access to login page."""

    flash('Page not found.', 'warning')

    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found_error(error):
    """Returns 404 error page."""

    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Returns 500 error page. Cancels uncommitted database changes."""

    db.session.rollback()

    return render_template('500.html'), 500
