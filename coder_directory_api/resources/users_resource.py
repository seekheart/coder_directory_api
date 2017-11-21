"""
Users Resource

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import flask
# from flask_restful import Resource
from flask_restful_swagger_2 import swagger, Resource
from coder_directory_api.engines import UsersEngine
from coder_directory_api.swagger import *

users_engine = UsersEngine()

class UserList(Resource):
    @swagger.doc({
        'tags': ['users'],
        'description': 'Returns all users',
        'parameters': [
            {
                'name': 'name',
                'description': 'Name to filter by',
                'type': 'string',
                'in': 'query'
            }
        ],
        'responses': {
            '200': {
                'description': 'List of users',
                'schema': UserModel,
                'examples': {
                    'application/json': [
                        {
                            'id': 1,
                            'name': 'somebody'
                        }
                    ]
                }
            }
        }
    })
    def get(self):
        return flask.make_response(
            _make_payload(users_engine.find_all()),
            200
        )

    def post(self):
        data = flask.request.get_json()
        if not data:
            flask.abort(400)
        try:
            result = users_engine.add_one(data)
            if result:
                new_user = users_engine.find_one(result)
                user_id = {'id': new_user['_id']}
                return flask.make_response(_make_payload(user_id), 201)
            else:
                return flask.make_response(
                    _make_payload({'message': 'Not modified'}),
                    304)
        except AttributeError as e:
            return flask.make_response(
                    _make_payload({'message': 'User Exists!'}),
                    409
            )


class User(Resource):
    def get(self, user_id: int):
        payload = users_engine.find_one(user_id)
        if not payload:
            return flask.make_response(
                _make_payload({'message': 'User not found'}),
                404
            )
        return _make_payload(payload)

    def delete(self, user_id: int):
        try:
            doc = users_engine.find_one(user_id)['_id']
            result = users_engine.delete_one(doc)
        except TypeError as e:
            result = False
        except AttributeError as e:
            result = False
        if result:
            return flask.make_response(
                _make_payload({'message': 'Accepted'}),
                202
            )
        else:
            return flask.make_response(
                _make_payload({'message': 'User not found!'}),
                404)


def _make_payload(p):
    return flask.jsonify(p)
