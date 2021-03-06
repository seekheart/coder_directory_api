"""
Users resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask import abort, request, Blueprint, jsonify
from coder_directory_api.engines import UsersEngine
from coder_directory_api.auth import token_required

# setup the users resource
api = Blueprint('users', __name__)

# Instantiate database engine
users_engine = UsersEngine()


@api.route('/', methods=['GET', 'POST'])
@token_required
def users_list()-> tuple:
    """GET and POST Operations for Users Resource.
    For POST, data must be posted in JSON format.

    Returns:
        Tuple containing json msg or data with status code.
    """
    if request.method == 'GET':
        users = users_engine.find_all()
        return jsonify(users), 200
    elif request.method == 'POST':
        data = None
        try:
            data = request.get_json()
        except ValueError as e:
            abort(400)
        try:
            result = users_engine.add_one(data)
            if result:
                new_user = users_engine.find_one(result)
                user_id = new_user['_id']
                msg = {
                           'message': 'successfully added new user',
                           'user_id': user_id
                       }

                return jsonify(msg), 201
            else:
                msg = {'message': 'Not modified'}
                return jsonify(msg), 304
        except AttributeError as e:
            msg = {'message': 'User exists!'}
            return jsonify(msg), 409
    else:
        abort(400)


@api.route('/<int:user_id>', methods=['GET', 'DELETE', 'PATCH'])
@token_required
def user_single(user_id: int) -> tuple:
    """GET, PATCH, DELETE operations for a single User of Users Resource by user
    id.

    Args:
        user_id: unique id of a user to perform operations on.

    Returns:
        Tuple containing json data or message with http status code.
    """

    user = users_engine.find_one(user_id)
    if not user:
        msg = {'message': 'User Not Found'}
        return jsonify(msg), 404
    if request.method == 'GET':
        return jsonify(user), 200

    elif request.method == 'DELETE':
        try:
            result = users_engine.delete_one(user_id)
        except TypeError as e:
            result = False
        except AttributeError as e:
            result = False
        if result:
            msg = {'message': 'Accepted'}
            return jsonify(msg), 202
        else:
            msg = {'message': 'User Not Found'}
            return jsonify(msg), 404
    elif request.method == 'PATCH':
        try:
            data = request.get_json()
            result = users_engine.edit_one(user_id, data)
        except AttributeError as e:
            msg = {'message': 'Internal Server Error'}
            return jsonify(msg), 400

        if result:
            msg = {'message': 'No Content'}
            return jsonify(msg), 204
        else:
            msg = {'message': 'Unprocessable Entity'}
            return jsonify(msg), 422
    else:
        abort(400)
