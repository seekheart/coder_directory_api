"""
Languages resource for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask import Blueprint
import json

api = Blueprint('/', __name__)

@api.route('/')
def home() -> tuple:
    """Home resource returns all available api resources in JSON

    Returns:
        Tuple with json containing resources available and http status code.
    """


    available = [
        {
            'languages': 'Programming languages resource',
            'users': 'Users resource'
        }
    ]

    return json.dumps(available), 200
