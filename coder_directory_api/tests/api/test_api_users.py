"""
Tests for Users Resource of Coder Directory app

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from .common_test_setup import CommonApiTest
import json
import coder_directory_api.engines as engines


class UsersResourceTest(CommonApiTest):
    def setUp(self):
        """Setup Users Tests"""
        super(UsersResourceTest, self).setUp()
        self.endpoint = '{}/users'.format(self.base_url)
        self.engine = engines.UsersEngine()
        self.dummy = {
            '_id': 9999,
            'username': 'dummy',
            'languages': [1]
        }
        self.dummy = json.dumps(self.dummy)
    
    def tearDown(self):
        """Teardown Users Tests"""
        super(UsersResourceTest, self).tearDown()
        try:
            self.engine.delete_one(9999)
        except AttributeError:
            pass
        self.engine = None

    def test_get_all_users(self):
        """test users endpoint for list of users"""
        result = self.app.get(self.endpoint)
        self.assertEquals(
            result.status_code,
            200,
            msg='Expected 200 status code'
        )
        self.assertTrue(
            result,
            msg='Expected user endpoint to have data'
        )

    def test_get_one_user(self):
        """test getting one specific user from users resource"""
        result = self.app.get('{}/1'.format(self.endpoint))
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
        """test adding a user to users resource"""
        result = self.app.post(
            self.endpoint,
            data=self.dummy,
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
        """test if api can prevent adding duplicate user to users resource"""
        self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )
        result = self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )

        self.assertEqual(
            result.status_code,
            409,
            msg='Expected status code to be 409'
        )

    def test_post_non_existing_user(self):
        """test if api can handle no payload post to users resource"""
        result = self.app.post(
            self.endpoint,
            data=None,
            content_type='application/json'
        )

        self.assertEquals(
            result.status_code,
            400,
            msg='Expected 400 status code abort'
        )

    def test_delete_user(self):
        """test if a user can be deleted"""
        self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )

        result = self.app.delete(
            '{}/9999'.format(self.endpoint)
        )

        self.assertEqual(
            result.status_code,
            202,
            'Expected dummy user to be deleted'
        )

    def test_delete_no_user(self):
        """test if a invalid user is deletable from users resource"""
        result = self.app.delete('{}/44444444'.format(self.endpoint))

        self.assertEqual(
            result.status_code,
            404,
            msg='Expected to not find user to delete'
        )

    def test_edit_one_user(self):
        """test if a user of users resource can be edited"""
        self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )

        modification = json.dumps({'username': 'dummy2'})

        result = self.app.patch(
            '{}/9999'.format(self.endpoint),
            data=modification,
            content_type='application/json'
        )

        self.assertEquals(result.status_code, 204)

        data = self.app.get('{}/9999'.format(self.endpoint))

        self.assertEqual(
            data.status_code,
            200,
            'expected dummy2 to exist after patch'
        )
