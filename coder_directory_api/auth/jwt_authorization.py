"""
JWT Based Authentication

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import datetime
import jwt
import functools
from flask import request, jsonify
import coder_directory_api.settings as settings
import coder_directory_api.engines as engines
import uuid

# set some global helpers
auth_engine = engines.AuthEngine()
secret = settings.SECRET_KEY
expire_time = datetime.timedelta(minutes=5)


def refresh_token(token) -> dict or None:
    """
    JWT access token refresh method.

    Args:
        token: payload containing jwt access token to refresh and refresh token.

    Returns:
        refreshed jwt token payload.
    """
    user = token['user']
    user_refresh_token = token['refresh_token']

    try:
        jwt.decode(token['refresh_token'], secret)
    except (jwt.DecodeError, jwt.InvalidTokenError) as e:
        return None

    if user:
        ref_token = auth_engine.find_one(user=user)
    else:
        return None

    ref_token = ref_token['refresh_token']

    try:
        ref_token = ref_token.decode('utf-8')
    except AttributeError:
        return None

    if ref_token == user_refresh_token:
        new_access_token = make_access_token(user)
        result = auth_engine.edit_one(
            user=user,
            doc={'access_token': new_access_token}
        )
    else:
        return None

    if result:
        user_doc = {
            'user': user,
            'access_token': new_access_token,
            'refresh_token': token['refresh_token']
        }
        return make_payload(user_doc=user_doc)
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
    ) as e:
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

    renew_token = make_refresh_token(user)
    access_token = make_access_token(user)

    tokens = {
        'access_token': access_token,
        'refresh_token': renew_token
    }

    auth_engine.edit_one(user=user, doc=tokens)
    user_doc = {
        'user': user,
        'access_token': tokens['access_token'],
        'refresh_token': tokens['refresh_token']
    }
    payload = make_payload(user_doc=user_doc)
    return payload


def make_timestamp() -> int:
    """
    Helper function to make timestamps.

    Returns:
        timestamp in milliseconds.
    """
    date = int(datetime.datetime.utcnow().strftime('%s')) * 1000
    return date


def make_payload(user_doc: dict) -> dict:
    """
    Helper function to make payload for jwt tokens.
    Args:
        user_doc: dictionary containing user, access_token, refresh_token

    Returns:
        api payload for jwt token.
    """

    try:
        access_token = user_doc['access_token'].decode('utf-8')
    except AttributeError:
        access_token = user_doc['access_token']

    try:
        renew_token = user_doc['refresh_token'].decode('utf-8')
    except AttributeError:
        renew_token = user_doc['refresh_token']
    return {
        'user': user_doc['user'],
        'created': datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
        'expires_in': expire_time.seconds,
        'access_token': access_token,
        'refresh_token': renew_token
    }


def make_access_token(user_name: str) -> dict:
    """
    Helper function to make the access token.

    Args:
        user_name: username to make token for.

    Returns:
        encrypted jwt access token
    """
    return jwt.encode(
        {
            'iss': 'coder directory',
            'user': user_name,
            'jti': str(uuid.uuid4()),
            'iat': make_timestamp(),
            'exp': datetime.datetime.utcnow() + expire_time
        },
        secret
    )


def make_refresh_token(user_name: str) -> dict:
    """
    Helper function to make refresh token.

    Args:
        user_name: username to make token for.

    Returns:
        encrypted jwt refresh token.
    """

    return jwt.encode(
        {
            'iss': 'coder directory',
            'sub': user_name,
            'created': datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S'),
            'jti': str(uuid.uuid4()),
            'iat': make_timestamp(),
        },
        secret)
