"""
Google OAuth for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""


from coder_directory_api.settings import GOOGLE, BASE_URL
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.google import google
from flask import redirect, url_for
from .google_auth_engine import GoogleAuthEngine
from functools import wraps


# backend = GoogleAuthEngine()
google_bp = make_google_blueprint(
    client_id=GOOGLE['client_id'],
    client_secret=GOOGLE['client_secret'],
    scope=['profile', 'email'],
    redirect_url=BASE_URL,
    # backend=backend
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

