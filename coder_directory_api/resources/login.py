"""
Login resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask import Blueprint, jsonify, request
from coder_directory_api.engines import AuthEngine
import coder_directory_api.auth as auth

api = Blueprint('login', __name__)
auth_engine = AuthEngine()


@api.route('/', methods=['GET', 'POST'])
def login() -> tuple:
    """Login resource allows users to login and retrieve an auth token.

    Returns:
        Tuple with json containing token or message with http status code.
    """

    if request.method == 'GET':
        message = {'message': 'Please send user and password for login'}
        return jsonify(message), 200
    elif request.method == 'POST':
        user = request.json
        user_doc = auth_engine.find_one(user['user'])

        if user_doc and user_doc['password'] == user['password']:
            payload = auth.make_token(user_doc['user'])
            payload = jsonify(payload)
            return payload, 200
        else:
            message = {'message': 'Invalid user/password'}
            return jsonify(message), 400


@api.route('/token', methods=['GET', 'POST'])
def refresh() -> tuple:
    """
    Refresh token resource allows users to renew their access token before
    expiration.

    Returns:
        Tuple with json containing refreshed token or message with http status
        code.
    """

    if request.method == 'GET':
        message = {'message': 'Please send tokens to refresh access'}
        return jsonify(message), 200
    elif request.method == 'POST':
        data = request.json
        payload = auth.refresh_token(data)
        if payload is None:
            message = {'message': 'Access token has expired please re-login'}
            return jsonify(message), 400

        return jsonify(payload), 200
