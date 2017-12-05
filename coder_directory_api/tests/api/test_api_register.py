"""
Test for Register Resource

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from .common_test_setup import CommonApiTest
from coder_directory_api.engines import AuthEngine
import json


class RegisterResourceTest(CommonApiTest):
    def setUp(self):
        """Setup register resource test environment"""
        super(RegisterResourceTest, self).setUp()
        self.endpoint = '{}/register'.format(self.base_url)
        self.dummy = json.dumps({'user': 'testUser', 'password': 'defe'})
        self.engine = AuthEngine()

    def tearDown(self):
        super(RegisterResourceTest, self).tearDown()
        self.dummy = None
        try:
            self.engine.delete_one(user='testUser')
        except AttributeError:
            pass
        self.engine = None

    def test_register_user(self):
        """Test if user registration works"""
        result = self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )

        self.assertTrue(
            result,
            msg='Expected results to come back True'
        )

        self.assertEqual(
            result.status_code,
            201,
            msg='Expected status code to be 201 from registration'
        )

    def test_register_user_no_password(self):
        """Test if user registration works without password"""
        test = {'user': 'asdf'}
        result = self.app.post(
            self.endpoint,
            data=json.dumps(test),
            content_type='application/json'
        )

        self.assertEquals(
            result.status_code,
            400,
            msg='Expected 400 bad request from missing password'
        )

    def test_register_no_user(self):
        """Test if user registration works without password"""
        test = {'password': 'asdf'}
        result = self.app.post(
            self.endpoint,
            data=json.dumps(test),
            content_type='application/json'
        )

        self.assertEquals(
            result.status_code,
            400,
            msg='Expected 400 bad request from missing password'
        )
