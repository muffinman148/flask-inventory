"""
Creates reusable decorators for flask routes functions.

ex: @requires_access_level - Requires users to be a designated access level on
the corresponding function.
"""

from functools import wraps
from flask import url_for, request, redirect, session
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if not current_user.allowed(access_level):
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
