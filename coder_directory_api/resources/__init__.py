"""
REST resources for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""


__all__ = ['api_resources']
from .languages import api as languages_api
from .users import api as users_api
from .home import api as home_api

# Create a list of resource objects to register in api
api_resources = [
    {'bp': languages_api, 'route': 'languages'},
    {'bp': users_api, 'route': 'users'},
    {'bp': home_api, 'route': None}
]
