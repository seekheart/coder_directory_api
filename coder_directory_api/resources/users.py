"""
Users resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask_restplus import Namespace, Resource, fields
from flask import abort, request
from coder_directory_api.engines import UsersEngine
import json

# setup the users resource
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


@api.route('/')
class UserList(Resource):
    """This defines the users collection for GET and POST requests"""
    @api.marshal_list_with(user_model, mask=None)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        500: 'Internal Server error!',
    })
    def get(self) -> list:
        """Finds all users in the users resource"""
        return users_engine.find_all()

    @api.expect(user_model)
    @api.marshal_with(message_model, mask=None)
    @api.doc(responses={
        201: 'Successfully added new user',
        304: 'Not modified',
        409: 'User exists',
    })
    def post(self) -> tuple or dict:
        """Adds a user to the users collection
        if there is data in the request provided by caller.
        User_id is automatically added if not provided.
        """
        try:
            data = json.loads(request.data.decode('utf-8'))
        except ValueError as e:
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


@api.route('/<int:user_id>')
class User(Resource):
    """This provides GET, PATCH, and DELETE to a user in users collection"""
    @api.marshal_with(user_model, mask=None)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        404: 'User Not found',
        500: 'Internal server error',
    })
    def get(self, user_id: int) -> tuple or dict:
        """Gets one user based on the user_id provided

        Args:
            user_id: unique user identifier number.
        Returns:
            a message json with http status code.
        """
        payload = users_engine.find_one(user_id)
        if not payload:
            return {'message': 'User Not Found'}, 404
        return payload

    @api.marshal_with(message_model, mask=None)
    @api.doc(responses={
        202: 'Accepted',
        404: 'User Not Found',
        500: 'Internal server error',
    })
    def delete(self, user_id: int) -> tuple:
        """Deletes a user from the user resource by user_id.

        Args:
            user_id: unique user identifier number.

        Returns:
            a message json with http status code.
        """
        try:
            # doc = users_engine.find_one(user_id)['_id']
            result = users_engine.delete_one(user_id)
        except TypeError as e:
            print('TypeError', e)
            result = False
        except AttributeError as e:
            result = False
            print('AttributeError', e)
        if result:
            return {'message': 'Accepted'}, 202
        else:
            return {'message': 'User Not Found'}, 404

    @api.expect(user_model)
    @api.marshal_list_with(message_model, mask=None)
    @api.doc(responses={
        204: 'No Content',
        400: 'Bad Request',
        404: 'User not found',
        422: 'Unprocessable Entity',
        500: 'Internal server error'
    })
    def patch(self, user_id: int) -> tuple:
        """Edits a user from users resource by user_id.

        Args:
            user_id: unique user identifier number.

        Returns:
            a message json with http status code
        """

        try:
            data = json.loads(request.data.decode('utf-8'))
            user = users_engine.find_one(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            result = users_engine.edit_one(user_id, data)
        except AttributeError as e:
            return {'message': 'Bad Request'}, 400

        if result:
            return {'message': 'No Content'}, 204
        else:
            return {'message': 'Unprocessable Entity'}, 422

