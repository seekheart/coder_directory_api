"""
REST resources for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask_restplus import Api
from flask import Blueprint
from .users import api as users_api
from .languages import api as languages_api
from coder_directory_api.settings import BASE_URL


# Register Blueprint for app based on all available resources
blueprint = Blueprint('api', __name__, url_prefix=BASE_URL)
api = Api(
    blueprint,
    version='1.0.0',
    title='Coder Directory Api',
    description='A coder directory rest api for managing coders'
)

# Register resource with api name space
api.add_namespace(users_api)
api.add_namespace(languages_api)
