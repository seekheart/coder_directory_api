"""
Test for Login Resource

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from .common_test_setup import CommonApiTest
from coder_directory_api.engines import AuthEngine
import json


class LoginResourceTest(CommonApiTest):
    def setUp(self):
        """Setup login resource test environment"""
        super(LoginResourceTest, self).setUp()
        self.endpoint = '{}/login'.format(self.base_url)
        self.dummy = {'user': 'test', 'password': 'defe'}
        self.engine = AuthEngine()

        self.engine.add_one(self.dummy)
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
            result.status_code,
            200,
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
            result.status_code,
            200,
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
            result.status_code,
            400,
            msg='Expected invalid user/password 400 status code'
        )