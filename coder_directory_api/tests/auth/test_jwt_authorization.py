"""
Test for JWT Authorization

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details
"""

import coder_directory_api.auth as auth
import coder_directory_api.settings as settings
from coder_directory_api.engines import AuthEngine
import unittest
import jwt
import datetime
import uuid


class JwtAuthorizationTest(unittest.TestCase):
    def setUp(self):
        """Set up each test environment prior to running"""
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

        self.dummy = {
            'user': 'test_dummy',
            'password': 'asdf',
            'access_token': jwt.encode(
                    self.dummy_access,
                    settings.SECRET_KEY
                ).decode('utf-8'),
            'refresh_token': jwt.encode(
                    self.dummy_refresh,
                    settings.SECRET_KEY
                ).decode('utf-8')
        }

        self.engine = AuthEngine()
        self.engine.add_one(self.dummy)

    def tearDown(self):
        """Clean up jwt authorization tests"""
        try:
            self.engine.delete_one('test_dummy')
        except AttributeError:
            pass
        self.engine = None


    def test_check_token(self):
        """Test validating a jwt token"""
        result = auth.check_token(
            jwt.encode(self.dummy_access, settings.SECRET_KEY)
        )
        self.assertTrue(
            result,
            msg='Expected valid token to return true'
        )

    def test_expired_token(self):
        """Test validating an expired token"""
        token = self.dummy_access
        token['exp'] = 1000
        result = auth.check_token(jwt.encode(token, settings.SECRET_KEY))

        self.assertFalse(
            result,
            msg='Expected invalid expired token to return false'
        )

    def test_invalid_token(self):
        """Test an invalid token"""
        token = {'hi': 123, 'user': 'nininio;n'}
        result = auth.check_token(jwt.encode(token, settings.SECRET_KEY))
        self.assertFalse(
            result,
            msg='Expected invalid token to return false'
        )

    def test_wrong_signature(self):
        """Test authorization with wrong signature"""
        result = auth.check_token(jwt.encode(self.dummy_access, 'no'))
        self.assertFalse(
            result,
            msg='Expected invalid signature to return false'
        )