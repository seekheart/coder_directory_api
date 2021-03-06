"""
Languages resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from coder_directory_api.engines import LanguagesEngine
from flask import abort, request, jsonify, Blueprint
from coder_directory_api.auth import token_required

# setup language resource blueprint
api = Blueprint('languages', __name__)

# Instantiate database engine
language_engine = LanguagesEngine()


# Define routes
@api.route('/', methods=['GET', 'POST'])
@token_required
def language_list() -> tuple:
    """GET and POST operations on Languages Resource.
    For POST, data must be in json format.

    Returns:
        Tuple containing json message or data with status code.
    """

    if request.method == 'GET':
        data = jsonify(language_engine.find_all())
        return data, 200
    elif request.method == 'POST':
        try:
            data = request.get_json()
        except ValueError as e:
            abort(400)
        try:
            result = language_engine.add_one(data)
            if result:
                msg = {
                    'message': 'Successfully added new language',
                    'language_id': result
                }
                return jsonify(msg), 201
            else:
                msg = {'message': 'Not Modified'}
                return jsonify(msg), 304
        except AttributeError as e:
            msg = {'message': 'Language exists or is Synonym'}
            return jsonify(msg), 409
    else:
        abort(400)


@api.route('/<int:language_id>', methods=['GET', 'DELETE', 'PATCH'])
@token_required
def language_single(language_id: int) -> tuple:
    """GET, DELETE, PATCH operations for a single language given a language_id

    Args:
        language_id: unique id for a language.

    Returns:
        a json with the data if found or a message if not found.
    """

    payload = language_engine.find_one(language_id)
    if not payload:
        msg = jsonify({'message': 'Language Not Found'})
        return msg, 404

    if request.method == 'GET':

        return jsonify(payload), 200
    elif request.method == 'DELETE':
        try:
            result = language_engine.delete_one(language_id)
        except TypeError as e:
            result = False
        except AttributeError as e:
            result = False

        if result:
            msg = {'message': 'Accepted'}
            return jsonify(msg), 202
        else:
            msg = {'message': 'Internal Error'}
            return jsonify(msg), 500
    elif request.method == 'PATCH':
        try:
            data = request.get_json()
            result = language_engine.edit_one(language_id, data)
        except AttributeError as e:
            msg = {'message': 'Bad Request'}
            return jsonify(msg), 400
        if result:
            msg = {'message': 'No Content'}
            return jsonify(msg), 204
        else:
            msg = {'message': 'Unprocessable Entity'}
            return jsonify(msg), 422
    else:
        abort(400)
