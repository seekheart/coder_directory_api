"""
Register resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask import Blueprint,  jsonify, request
import engines

api = Blueprint('register', __name__)
auth_engine = engines.AuthEngine()


@api.route('/', methods=['GET', 'POST'])
def register() -> tuple:
    """register resource allows creation of user accounts for access to
    protected resources.

    Returns:
        Tuple with json containing token or message with http status code.
    """

    if request.method == 'GET':
        template = {'user': 'username', 'password': 'password'}
        message = {
            'message': 'please send following payload in POST to register',
            'template': template
        }
        return jsonify(message), 200
    elif request.method == 'POST':
        user = request.json

        if 'user' in user and 'password' in user:
            result = auth_engine.add_one(user)
        else:
            message = {'message': 'Missing user/password!'}
            return jsonify(message), 400

        if result:
            message = {'message': 'Successfully registered'}
            return jsonify(message), 201

        message = {'message': 'User {user} already exists'.format(**user)}
        return jsonify(message), 409







