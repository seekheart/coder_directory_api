"""
JWT Based Authentication

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import datetime
import jwt
import functools
from flask import request, jsonify
import settings
import engines
import uuid

# set some global helpers
auth_engine = engines.AuthEngine()
secret = settings.SECRET_KEY


def refresh_token(token) -> dict or None:
    """
    JWT access token refresh method.

    Args:
        token: payload containing jwt access token to refresh and refresh token.

    Returns:
        refreshed jwt token payload.
    """

    try:
        user = token['user']
        token['access_token'] = jwt.decode(token['access_token'], secret)
        token['refresh_token'] = jwt.decode(token['refresh_token'], secret)
    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
        return None

    ref_token = auth_engine.find_one(user=user)
    ref_token = ref_token['refresh_token']

    if ref_token == token['refresh_token']:
        token['access_token']['exp'] = datetime.datetime.utcnow() + \
                                       datetime.timedelta(minutes=5)
        result = auth_engine.edit_one(user=user, doc=token)
    else:
        return None

    token['access_token'] = jwt.encode(
                                token['access_token'], secret
                            ).decode('utf-8')
    token['refresh_token'] = jwt.encode(
                                token['refresh_token'], secret
                            ).decode('utf-8')


    if result:
        return token
    else:
        return None


def check_token(token) -> bool:
    """
    Checks the provided authorization header for token and validates.

    Args:
        token: Token provided in authorization header.

    Returns:
        Indicator as to whether token is valid or not.
    """

    result = True
    try:
        decoded_token = jwt.decode(token, secret)
    except (
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
            KeyError
    ):
        result = False
    else:
        user = auth_engine.find_one(decoded_token['user'])
        if not user:
            result = False

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
        result = True
        message = {'message': 'Unauthorized'}
        try:
            auth = request.headers['Authorization'].split(' ')[1]
        except KeyError:
            result = False
            auth = None
        if not auth:
            result = False

        state = check_token(auth)

        if not state:
            result = False

        if not result:
            return jsonify(message), 401

        return f(*args, **kwargs)

    return wrapper


def make_token(user: str) -> dict:
    """
    Makes jwt token for authenticated clients.

    Args:
        user: authenticated user to make token for.

    Returns:
        json message with tokens for authenticated clients and error message
        for unauthenticated clients.
    """

    renew_token = {
        'iss': 'coder directory',
        'sub': user,
        'created': datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S'),
        'jti': str(uuid.uuid4()),
        'iat': make_timestamp(),
    }

    access_token = {
        'iss': 'coder directory',
        'user': user,
        'jti': str(uuid.uuid4()),
        'iat': make_timestamp(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }

    tokens = {
        'access_token': access_token,
        'refresh_token': renew_token
    }

    auth_engine.edit_one(user=user, doc=tokens)

    payload = {
        'user': user,
        'created': datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S'),
        'access_token': jwt.encode(access_token, secret).decode('utf-8'),
        'refresh_token': jwt.encode(renew_token, secret).decode('utf-8')
    }

    return payload


def make_timestamp() -> int:
    """
    Helper function to make timestamps.

    Returns:
        timestamp in milliseconds.
    """
    date = int(datetime.datetime.utcnow().strftime('%s')) * 1000
    return date
