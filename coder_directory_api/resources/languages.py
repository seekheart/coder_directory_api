"""
Languages resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from coder_directory_api.engines import LanguagesEngine
from flask_restplus import Namespace, Resource, fields
from flask import abort, request, redirect, url_for
import json


# setup language resource
api = Namespace('languages', description='Languages resource')

#model registry
language_model = api.model('Language', {
    '_id': fields.Integer(readOnly=True, description='Language Id'),
    'name': fields.String(required=True, description='Language official name'),
    'synonyms': fields.List(
        fields.String(description='synonym names of language')
    ),
    'users': fields.List(
        fields.Integer(description='User Ids who know this language')
    )
})

message_model = api.model('Message', {
    'message': fields.String(description='Api message'),
    'language_id': fields.Integer(description='Language Id')
})

# Instantiate database engine
language_engine = LanguagesEngine()

# Define route resources


@api.route('/')
class LanguageList(Resource):
    """Language collection resource"""
    @api.marshal_list_with(language_model, mask=None)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        500: 'Internal Server Error'
    })
    def get(self) -> list:
        """Finds all languages available in language resource"""
        return language_engine.find_all()

    @api.expect(language_model)
    @api.marshal_with(message_model, mask=None)
    @api.doc(responses={
        201: 'Successfully added new language',
        304: 'Not Modified',
        409: 'Language Exists or Is Synonym',
    })
    def post(self) -> tuple or dict:
        """Adds a language to collection if it does not exist or is synonym"""
        try:
            data = request.get_json()
        except ValueError as e:
            abort(400)

        try:
            result = language_engine.add_one(data)
            if result:
                return {
                   'message': 'Successfully added new language',
                   'language_id': result
                       }, 201
            else:
                return {'message': 'Not Modified'}, 304
        except AttributeError as e:
            return {'message': 'Language exists or is Synonym'}, 409

@api.route('/<int:language_id>')
class Language(Resource):
    """Language collection resource for individual languages"""
    @api.marshal_with(language_model, mask=None)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        404: 'Language Not Found',
        500: 'Internal Server Error'
    })
    def get(self, language_id: int) -> tuple or dict:
        """Gets a single language given the language_id

        Args:
            language_id: unique id for a language.

        Returns:
            a json with the data if found or a message if not found.
        """

        payload = language_engine.find_one(language_id)
        if not payload:
            return {'message': 'Language not Found'}, 404
        return payload

    @api.marshal_with(message_model, mask=None)
    @api.doc(responses={
        202: 'Accepted',
        404: 'Language Not Found',
        500: 'Internal server error',
    })
    def delete(self, language_id: int) -> tuple:
        """Deletes a language from the language resource given a language_id

        Args:
            language_id: unique id for a language.

        Returns:
            a message json with http status code.
        """

        is_exist = language_engine.find_one(language_id)

        if not is_exist:
            return {'message': 'Language Not Found'}, 404
        try:
            result = language_engine.delete_one(language_id)
        except TypeError as e:
            print(e)
            result = False
        except AttributeError as e:
            print(e)
            result = False

        if result:
            return {'message': 'Accepted'}, 202
        else:
            return {'message': 'Language Not Found'}, 404

    @api.expect(language_model)
    @api.marshal_with(message_model, mask=None)
    @api.doc(responses={
        204: 'No Content',
        400: 'Bad Request',
        404: 'User Not Found',
        422: 'Unprocessable Entity',
        500: 'Internal server error'
    })
    def patch(self, language_id: int) -> tuple:
        """Edits a language from languages resource by language_id

        Args:
            language_id: unique language identifier

        Returns:
            a message json with http status code
        """
        try:
            data = request.get_json()
            lang = language_engine.find_one(language_id)
            if not lang:
                return {'message': 'Language Not Found!'}, 404
            result = language_engine.edit_one(language_id, data)
        except AttributeError as e:
            return {'message': 'Bad Request'}

        if result:
            return {'message': 'No Content'}, 204
        else:
            return {'message': 'Unprocessable Entity'}, 422
