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
        return json.dumps(message), 200
    elif flask.request.method == 'POST':
        user = flask.request.json
        user_doc = auth_engine.find_one(user['user'])

        if user_doc and user_doc['password'] == user['password']:
            try:
                payload = {
                    'access_token': user_doc['access_token'],
                    'refresh_token': user_doc['refresh_token']
                }
            except KeyError:
                payload = auth.make_token(user_doc['user'])
            finally:
                payload = json.dumps(payload)
                return payload
        else:
            message = {'message': 'Invalid user/password'}
            return json.dumps(message), 400

