"""
Common Setup for all Api Tests

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from coder_directory_api.api import create_app
from coder_directory_api.settings import BASE_URL, SECRET_KEY
from coder_directory_api.engines import AuthEngine
import datetime
import jwt
import uuid
import unittest


class CommonApiTest(unittest.TestCase):
    """Common Api Test Case for testing api behavior"""
    def setUp(self):
        """Common setup for api tests"""
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CRSF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = BASE_URL

        self.auth_engine = AuthEngine()
        self.dummy_access = {
            'iss': 'coder directory',
            'user': 'test_dummy',
            'jti': str(uuid.uuid4()),
            'iat': int(datetime.datetime.utcnow().strftime('%s')) * 1000,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }

        self.dummy_refresh = {
            'iss': 'coder directory',
            'user': 'test_dummy',
            'jti': str(uuid.uuid4()),
            'iat': int(datetime.datetime.utcnow().strftime('%s')) * 1000,
            'created': datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S')
        }

        self.dummy_auth = {
            'user': 'test_dummy',
            'password': 'asdf',
            'access_token': jwt.encode(
                self.dummy_access,
                SECRET_KEY
            ).decode('utf-8'),
            'refresh_token': jwt.encode(
                self.dummy_refresh,
                SECRET_KEY
            ).decode('utf-8')
        }

        self.auth_engine.add_one(self.dummy_auth)
        self.token = self.dummy_auth['access_token']

    def tearDown(self):
        """Common teardown methods for api tests"""
        self.app = None
        try:
            self.auth_engine.delete_one('test_dummy')
        except AttributeError:
            pass
        self.auth_engine = None
