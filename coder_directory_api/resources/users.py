"""
Users resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask_restplus import Namespace, Resource, fields
from flask import abort, request
from coder_directory_api.engines import UsersEngine
import json

api = Namespace('users', description='Users resource')

# model registry
profile_model = api.model('UserProfile',
                          {
                              'bio': fields.String(description='User profile'),
                              'learning': fields.List(
                                  fields.String(
                                      required=False,
                                      description='Learning languages'))
                          }
                          )

user_model = api.model('User', {
    "_id": fields.Integer(readOnly=True,
                          description='User Id'),
    "languages": fields.List(
        fields.String(
            required=False,
            description='list of programming languages'
        )
    ),
    "profile": fields.Nested(profile_model),
    "username": fields.String(
        required=True,
        description='User name'
    )
})

message_model = api.model('Message', {
    'message': fields.String(description='Api message'),
    'user_id': fields.Integer(description='User Id')
})

# Instantiate database engine
users_engine = UsersEngine()


@api.route('/users')
class UserList(Resource):
    @api.marshal_list_with(user_model, mask=None)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        500: 'Internal server error!',
    })
    def get(self):
        return users_engine.find_all()

    @api.expect(user_model)
    @api.marshal_with(message_model, mask=None)
    @api.doc(responses={
        201: 'Successfully added new user',
        304: 'Not modified',
        409: 'User exists',
    })
    def post(self):
        data = json.loads(request.data.decode('utf-8'))
        if not data:
            abort(400)
        try:
            result = users_engine.add_one(data)
            if result:
                new_user = users_engine.find_one(result)
                user_id = new_user['_id']
                return {
                           'message': 'successfully added new user',
                           'user_id': user_id
                       }, 201
            else:
                return {'message': 'Not modified'}, 304
        except AttributeError as e:
            return {'message': 'User exists!'}, 409


@api.route('/users/<int:user_id>')
class User(Resource):
    @api.marshal_with(user_model, mask=None)
    @api.doc(responses={
        200: 'Success',
        404: 'User not found',
        500: 'Internal server error',
    })
    def get(self, user_id: int):
        payload = users_engine.find_one(user_id)
        if not payload:
            return {'message': 'User not found'}, 404
        return payload

    @api.marshal_list_with(message_model, mask=None)
    @api.doc(responses={
        202: 'Accepted',
        404: 'User not found',
        500: 'Internal server error',
    })
    def delete(self, user_id: int):
        try:
            doc = users_engine.find_one(user_id)['_id']
            result = users_engine.delete_one(doc)
        except TypeError as e:
            print('TypeError', e)
            result = False
        except AttributeError as e:
            result = False
            print('AttributeError', e)
        if result:
            return {'message': 'Accepted'}, 202
        else:
            return {'message': 'User not found'}, 404
