"""
Test for JWT Authorization

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details
"""

import coder_directory_api.auth as auth
import coder_directory_api.settings as settings
import unittest
import jwt
import datetime

class TestJwtAuthorization(unittest.TestCase):
    def setUp(self):
        """Set up each test environment prior to running"""

        self.dummy = {
            "user": "seekheart",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            "accessToken": "123",
            "refreshToken": "abc"
        }

    def test_check_token(self):
        """Test validating a jwt token"""
        result = auth.check_token(jwt.encode(self.dummy, settings.SECRET_KEY))
        self.assertTrue(
            result,
            msg='Expected valid token to return true'
        )

    def test_expired_token(self):
        """Test validating an expired token"""
        token = self.dummy
        token['exp'] = 1000
        result = auth.check_token(jwt.encode(token, settings.SECRET_KEY))

        self.assertFalse(
            result,
            msg='Expected invalid expired token to return false'
        )

    def test_invalid_token(self):
        """Test an invalid token"""
        token = {'hi': 123}
        result = auth.check_token(jwt.encode(token, settings.SECRET_KEY))
        self.assertFalse(
            result,
            msg='Expected invalid token to return false'
        )

    def test_wrong_signature(self):
        """Test authorization with wrong signature"""
        result = auth.check_token(jwt.encode(self.dummy, 'no'))
        self.assertFalse(
            result,
            msg='Expected invalid signature to return false'
        )