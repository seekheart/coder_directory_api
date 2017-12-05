"""
Register resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import json
import coder_directory_api.engines as engines

api = flask.Blueprint('register', __name__)
auth_engine = engines.AuthEngine()


@api.route('/', methods=['GET', 'POST'])
def register() -> tuple:
    """register resource allows creation of user accounts for access to
    protected resources.

    Returns:
        Tuple with json containing token or message with http status code.
    """

    if flask.request.method == 'GET':
        template = {'user': 'username', 'password': 'password'}
        message = {
            'message': 'please send following payload in POST to register',
            'template': template
        }
        return json.dumps(message), 200
    elif flask.request.method == 'POST':
        user = flask.request.json

        if 'user' in user and 'password' in user:
            result = auth_engine.add_one(user)
        else:
            message = {'message': 'Missing user/password!'}
            return json.dumps(message), 400

        if result:
            message = {'message': 'Successfully registered'}
            return json.dumps(message), 201

        message = {'message': 'User {user} already exists'.format(**user)}
        return json.dumps(message), 409







