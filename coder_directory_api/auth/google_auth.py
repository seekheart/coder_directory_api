"""
Google OAuth for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.google import google
from flask import redirect, url_for
from .google_auth_engine import GoogleAuthEngine
from functools import wraps


backend = GoogleAuthEngine()
google_bp = make_google_blueprint(
    client_id='551381493649-bh5ll1k1433ob4t2u0bsearqt4ul81q0.apps.googleusercontent.com',
    client_secret='uJJejrWskjy1U8OU0zRcdiNR',
    scope=['profile', 'email'],
    redirect_url='/api',
    backend=backend
)


def authorized(f):
    """Wrapper for OAuth via Google"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not google.authorized:
            return redirect(url_for('google.login'))
        else:
            return f(*args, **kwargs)

    return wrapped

