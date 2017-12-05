"""
Login resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import json
import coder_directory_api.engines as engines
import coder_directory_api.auth as auth

api = flask.Blueprint('login', __name__)
auth_engine = engines.AuthEngine()


@api.route('/', methods=['GET', 'POST'])
def login() -> tuple:
    """Login resource allows users to login and retrieve an auth token.

    Returns:
        Tuple with json containing token or message with http status code.
    """

    if flask.request.method == 'GET':
        message = {'message': 'Please send user and password for login'}
        return flask.jsonify(message), 200
    elif flask.request.method == 'POST':
        user = flask.request.json
        user_doc = auth_engine.find_one(user['user'])

        if user_doc and user_doc['password'] == user['password']:
            payload = auth.make_token(user_doc['user'])
            payload = flask.jsonify(payload)
            return payload, 200
        else:
            message = {'message': 'Invalid user/password'}
            return flask.jsonify(message), 400


@api.route('/token', methods=['GET', 'POST'])
def refresh() -> tuple:
    """
    Refresh token resource allows users to renew their access token before
    expiration.

    Returns:
        Tuple with json containing refreshed token or message with http status
        code.
    """

    if flask.request.method == 'GET':
        message = {'message': 'Please send tokens to refresh access'}
        return flask.jsonify(message), 200
    elif flask.request.method == 'POST':
        data = flask.request.json
        payload = auth.refresh_token(data)
        if payload is None:
            message = {'message': 'Access token has expired please re-login'}
            return flask.jsonify(message), 400

        return flask.jsonify(payload), 200
