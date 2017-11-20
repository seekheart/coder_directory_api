"""Api
This is the main entry point.

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
import coder_directory_api.settings as settings
import coder_directory_api.engines as engines


# Bootstrap api and engines
api = flask.Flask('__name__')
users_engine = engines.UsersEngine()

@api.route('/')
def home():
    return 'success!'


@api.route('/users', methods=['GET', 'POST'])
def users():
    if flask.request.method == 'GET':
        payload = users_engine.find_all()
        return _make_payload(payload)
    elif flask.request.method == 'POST':
        data = flask.request.get_json()
        try:
            result = users_engine.add_one(data)
            if result:
                new_user = users_engine.find_by_username(data['username'])
                user_id = new_user['_id']
                return _make_payload(user_id), 201
            else:
                return '', 304
        except AttributeError as e:
            return 'User Exists!', 409


@api.route('/users/<int:user_id>', methods=['GET', 'PATCH', 'DELETE'])
def username(user_id: int):
    if flask.request.method == 'GET':
        payload = users_engine.find_one(user_id)

        if not payload:
            return _make_payload({'message': 'User not found'}), 404
        return _make_payload(payload)
    elif flask.request.method == 'DELETE':
        try:
            doc = users_engine.find_one(user_id)['_id']
            result = users_engine.delete_one(doc)
        except TypeError as e:
            result = False
        except AttributeError as e:
            return '', 202

        if result:
            return '', 204
        else:
            return 'User not found!', 404
    elif flask.request.method == 'PATCH':
        try:
            doc = users_engine.find_one(user_id)['_id']
            data = flask.request.get_json()
            result = users_engine.edit_one(doc, data)

            if result:
                return '', 204
            else:
                return '', 422
        except TypeError as e:
            return 'User not found!', 404
        except AttributeError as e:
            return '', 400


def _make_payload(p):
    return flask.jsonify(p)


if __name__ == '__main__':
    api.run(host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            threaded=settings.MULTITHREADING)