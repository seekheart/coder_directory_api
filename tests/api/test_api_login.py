"""
Test for Login Resource

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from .common_test_setup import CommonApiTest
from coder_directory_api.engines import AuthEngine
from coder_directory_api.auth import make_token
import json


class LoginResourceTest(CommonApiTest):
    def setUp(self):
        """Setup login resource test environment"""
        super(LoginResourceTest, self).setUp()
        self.endpoint = '{}/login'.format(self.base_url)
        self.dummy = {
            'user': 'test',
            'password': 'defe'
        }
        self.engine = AuthEngine()

        self.engine.add_one(self.dummy)
        dummy_tokens = make_token('test')
        self.dummy = self.engine.find_one(user='test')
        self.dummy['access_token'] = dummy_tokens['access_token']
        self.dummy['refresh_token'] = dummy_tokens['refresh_token']
        self.dummy = json.dumps(self.dummy)

    def tearDown(self):
        """Teardown Login Tests"""
        super(LoginResourceTest, self).tearDown()
        self.dummy = None
        try:
            self.engine.delete_one(user='test')
        except AttributeError:
            pass
        self.engine = None

    def test_get(self):
        """Test a GET request on login resource"""
        result = self.app.get(self.endpoint)

        self.assertEqual(
            200,
            result.status_code,
            msg='Expected GET request to return 200 status'
        )

    def test_post_right(self):
        """Test POST request with proper login"""
        result = self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )

        self.assertTrue(
            result,
            msg='Expected api to return results'
        )

        self.assertEqual(
            200,
            result.status_code,
            msg='expected api to accept json payload'
        )

        self.assertTrue(
            result.data,
            msg='Expected token to be returned in json response'
        )

    def test_post_wrong(self):
        """Test POST request with wrong login"""
        result = self.app.post(
            self.endpoint,
            data={'user': 'bob'},
            content_type='application/json'
        )
        self.assertEqual(
            400,
            result.status_code,
            msg='Expected invalid user/password 400 status code'
        )


    def test_refresh_token(self):
        """Test if POST request can refresh a token"""
        result = self.app.post(
            '{}/token'.format(self.endpoint),
            data=self.dummy,
            content_type='application/json'
        )

        self.assertEqual(
            200,
            result.status_code,
            msg='Expected status code to be 200'
        )

        data = json.loads(result.data.decode('utf-8'))
        self.assertEqual(
            5,
            len(data),
            msg='Expected payload of 4 keys to return'
        )

    def test_bad_token(self):
        """Test if POST request will bounce bad tokens"""
        dummy = json.loads(self.dummy)
        dummy['refresh_token'] = None
        dummy = json.dumps(dummy)

        result = self.app.post(
            '{}/token'.format(self.endpoint),
            data=dummy,
            content_type='application/json'
        )

        self.assertEqual(
            400,
            result.status_code,
            msg='Expected token refresh to fail.'
        )
