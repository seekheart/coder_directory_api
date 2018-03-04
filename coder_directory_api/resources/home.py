"""
Home resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask import Blueprint, jsonify

api = Blueprint('/', __name__)


@api.route('/')
def home() -> tuple:
    """Home resource returns all available api resources in JSON

    Returns:
        Tuple with json containing resources available and http status code.
    """

    available = [
        {
            'languages': 'Programming languages resource.',
            'users': 'Users resource.',
            'login': 'Login to api for access.',
            'register': 'Registration route for access to api.',
            'google': 'OAuth2 Google sign in for access'
        }
    ]

    return jsonify(available), 200
