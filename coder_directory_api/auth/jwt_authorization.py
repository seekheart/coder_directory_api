"""
JWT Based Authentication

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import jwt
import functools
import flask
import json
import coder_directory_api.settings as settings
import coder_directory_api.engines as engines


auth_engine = engines.AuthEngine()


def check_token(token) -> bool:
    """
    Checks the provided authorization header for token and validates.

    Args:
        token: Token provided in authorization header.

    Returns:
        Indicator as to whether token is valid or not.
    """
    secret = settings.SECRET_KEY
    result = True
    try:
        decoded_token = jwt.decode(token, secret)
        user = auth_engine.find_one(decoded_token['user'])
    except (
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
            KeyError
    ):
        result = False
    else:
        if not user:
            auth_engine.add_one(decoded_token)

    return result


def token_required(f):
    """
    Decorated view function for adding token based authorization

    Args:
        f: View function to wrap.

    Returns:
        The view function if authorized else 401 http response.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth = flask.request.authorization
        message = {'message': 'Unauthorized'}
        if not auth:
            return json.dumps(message), 401

        state = check_token(auth)

        if not state:
            return json.dumps(message), 401

        return f(*args, **kwargs)
    return wrapper



