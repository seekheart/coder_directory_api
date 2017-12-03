"""
Languages resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import coder_directory_api.engines as engines
import flask
import json

# setup language resource blueprint
api = flask.Blueprint('languages', __name__)

# Instantiate database engine
language_engine = engines.LanguagesEngine()


# Define routes
@api.route('/', methods=['GET', 'POST'])
def language_list() -> tuple:
    """GET and POST operations on Languages Resource.
    For POST, data must be in json format.

    Returns:
        Tuple containing json message or data with status code.
    """

    if flask.request.method == 'GET':
        data = json.dumps(language_engine.find_all())
        return data, 200
    elif flask.request.method == 'POST':
        try:
            data = flask.request.get_json()
        except ValueError as e:
            flask.abort(400)
        try:
            result = language_engine.add_one(data)
            if result:
                msg = {
                    'message': 'Successfully added new language',
                    'language_id': result
                }
                return json.dumps(msg), 201
            else:
                msg = {'message': 'Not Modified'}
                return json.dumps(msg), 304
        except AttributeError as e:
            msg = {'message': 'Language exists or is Synonym'}
            return json.dumps(msg), 409
    else:
        flask.abort(400)


@api.route('/<int:language_id>', methods=['GET', 'DELETE', 'PATCH'])
def language_single(language_id: int) -> tuple:
    """GET, DELETE, PATCH operations for a single language given a language_id

    Args:
        language_id: unique id for a language.

    Returns:
        a json with the data if found or a message if not found.
    """

    payload = language_engine.find_one(language_id)
    if not payload:
        msg = json.dumps({'message': 'Language Not Found'})
        return msg, 404

    if flask.request.method == 'GET':

        return json.dumps(payload), 200
    elif flask.request.method == 'DELETE':
        try:
            result = language_engine.delete_one(language_id)
        except TypeError as e:
            result = False
        except AttributeError as e:
            result = False

        if result:
            msg = {'message': 'Accepted'}
            return json.dumps(msg), 202
        else:
            msg = {'message': 'Internal Error'}
            return json.dumps(msg), 500
    elif flask.request.method == 'PATCH':
        try:
            data = flask.request.get_json()
            result = language_engine.edit_one(language_id, data)
        except AttributeError as e:
            msg = {'message': 'Bad Request'}
            return json.dumps(msg), 400
        if result:
            msg = {'message': 'No Content'}
            return json.dumps(msg), 204
        else:
            msg = {'message': 'Unprocessable Entity'}
            return json.dumps(msg), 422
    else:
        flask.abort(400)
