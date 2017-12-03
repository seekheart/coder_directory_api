"""
Login resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import json
import coder_directory_api.engines as engines


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
        # TODO add real user password authentication
        user = flask.request.json
        if user:
            return json.dumps({'fakeToken': 123}), 200
