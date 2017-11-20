"""
Tests for Coder Directory api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""
import unittest
from coder_directory_api import api
import json
import coder_directory_api.engines as engines

class ApiTest(unittest.TestCase):
    def setUp(self):
        """Sets up api prior to performing each test"""
        api.config['TESTING'] = True
        api.config['WTF_CRSF_ENABLED'] = False
        self.api = api.test_client()
        self.dummy_user = {
            '_id': 9999,
            'username': 'dummy',
            'languages': [1]
        }
        self.dummy_user = json.dumps(self.dummy_user)
        self.usr_engine = engines.UsersEngine()

        try:
            self.usr_engine.delete_one(9999)
        except AttributeError as e:
            pass

    def tearDown(self):
        """Clean up protocol for api after each test"""
        self.app = None
        self.usr_engine.delete_one(9999)

    def test_home(self):
        result = self.api.get('/')
        self.assertEquals(result.status_code,
                          200,
                          msg='Expected 200 status code')

    def test_users_endpoint(self):
        result = self.api.get('/users')
        self.assertEquals(
            result.status_code,
            200,
            msg='Expected 200 status code'
        )
        self.assertTrue(
            result,
            msg='Expected user endpoint to have data'
        )
        self.assertNotEqual(
            result,
            0,
            msg='Expected payload to not be empty'
        )

    def test_get_one_user(self):
        result = self.api.get('users/1')
        payload = json.loads(result.data.decode('utf-8'))
        self.assertEquals(
            result.status_code,
            200,
            msg='Expected 200 status code'
        )
        self.assertTrue(
            result.data,
            msg='Expected test1 user to be found'
        )
        self.assertEquals(
            payload['_id'],
            1,
            msg='Expected test1 user to have _id 1'
        )

    def test_post_user(self):
        result = self.api.post(
            '/users',
            data=self.dummy_user,
            content_type='application/json'
        )

        user_id = json.loads(result.data.decode('utf-8'))

        self.assertEqual(
            result.status_code,
            201,
            msg='expected dummy user to POST'
        )

        self.assertTrue(
            user_id,
            msg='expected response to have newly added user id returned'
        )

    def test_post_existing_user(self):
        self.api.post(
            '/users',
            data=self.dummy_user,
            content_type='application/json'
        )
        result = self.api.post(
            '/users',
            data=self.dummy_user,
            content_type='application/json'
        )

        self.assertEqual(
            result.status_code,
            409,
            msg='Expected status code to be 409'
        )

    def test_delete_user(self):
        self.api.post(
            '/users',
            data=self.dummy_user,
            content_type='application/json'
        )

        result = self.api.delete(
            '/users/9999'
        )

        self.assertEqual(
            result.status_code,
            204,
            'Expected dummy user to be deleted'
        )

    def test_delete_no_user(self):
        result = self.api.delete('/users/44444444')

        self.assertEqual(
            result.status_code,
            404,
            msg='Expected to not find user to delete'
        )

    def test_edit_one_user(self):
        self.api.post(
            '/users',
            data=self.dummy_user,
            content_type='application/json'
        )

        modification = {'username': 'dummy2'}

        self.api.patch(
            '/users/9999',
            data=modification,
            content_type='application/json'
        )

        data = self.api.get('/users/9999')

        self.assertEqual(
            data.status_code,
            200,
            'expected dummy2 to exist after patch'
        )
