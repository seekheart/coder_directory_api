"""
Tests for Coder Directory app

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""
import unittest
import json
import coder_directory_api.engines as engines
import coder_directory_api
from coder_directory_api.settings import BASE_URL


class AppTest(unittest.TestCase):

    def setUp(self):
        """Sets up app prior to performing each test"""
        app = coder_directory_api.create_app()
        app.config['TESTING'] = True
        app.config['WTF_CRSF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()


        # engines for clean up
        self.usr_engine = engines.UsersEngine()
        self.language_engine = engines.LanguagesEngine()

        # urls
        self.base_url = BASE_URL
        self.user_endpoint = '{}/users'.format(self.base_url)
        self.language_endpoint = '{}/languages'.format(self.base_url)

        # dummy data
        self.dummy_user = {
            '_id': 9999,
            'username': 'dummy',
            'languages': [1]
        }
        self.dummy_user = json.dumps(self.dummy_user)
        self.dummy_language = {
            "_id": 9999,
            "name": "test3",
            "synonyms": ["asdf", "fefe"],
            "users": [9999]
        }
        self.dummy_language = json.dumps(self.dummy_language)

        try:
            self.usr_engine.delete_one(9999)
            self.language_engine.delete_one(9999)
        except AttributeError as e:
            pass

    def tearDown(self):
        """Clean up protocol for app after each test"""
        self.usr_engine.delete_one(9999)
        self.language_engine.delete_one(9999)
        self.usr_engine = None
        self.language_engine = None
        self.app = None

    def test_base_url(self):
        """test to make sure home endpoint exists"""
        result = self.app.get(self.base_url)
        self.assertEquals(
            result.status_code,
            200,
            msg='expected home url to give 200 status')

    def test_get_all_users(self):
        """test users endpoint for list of users"""
        result = self.app.get(self.user_endpoint)
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
        result = self.app.get('{}/1'.format(self.user_endpoint))
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
            self.user_endpoint,
            data=self.dummy_user,
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
            self.user_endpoint,
            data=self.dummy_user
        )
        result = self.app.post(
            self.user_endpoint,
            data=self.dummy_user
        )

        self.assertEqual(
            result.status_code,
            409,
            msg='Expected status code to be 409'
        )

    def test_post_non_existing_user(self):
        """test if api can handle no payload post to users resource"""
        result = self.app.post(
            self.user_endpoint,
            data=None,
        )

        self.assertEquals(
            result.status_code,
            400,
            msg='Expected 400 status code abort'
        )

    def test_delete_user(self):
        """test if a user can be deleted"""
        self.app.post(
            self.user_endpoint,
            data=self.dummy_user,
        )

        result = self.app.delete(
            '{}/9999'.format(self.user_endpoint)
        )

        self.assertEqual(
            result.status_code,
            202,
            'Expected dummy user to be deleted'
        )

    def test_delete_no_user(self):
        """test if a invalid user is deletable from users resource"""
        result = self.app.delete('{}/44444444'.format(self.user_endpoint))

        self.assertEqual(
            result.status_code,
            404,
            msg='Expected to not find user to delete'
        )

    def test_edit_one_user(self):
        """test if a user of users resource can be edited"""
        self.app.post(
            self.user_endpoint,
            data=self.dummy_user
        )

        modification = json.dumps({'username': 'dummy2'})

        result = self.app.patch(
            '{}/9999'.format(self.user_endpoint),
            data=modification
        )

        self.assertEquals(result.status_code, 204)

        data = self.app.get('{}/9999'.format(self.user_endpoint))

        self.assertEqual(
            data.status_code,
            200,
            'expected dummy2 to exist after patch'
        )

    def test_get_all_languages(self):
        """Test if all langauges in language resource can be gotten"""
        result = self.app.get(self.language_endpoint)

        self.assertEquals(
            result.status_code,
            200,
            msg='Expected 200 status on languages resource'
        )

    def test_get_one_language(self):
        """Test if a single language can be gotten from language resource"""
        result = self.app.get('{}/1'.format(self.language_endpoint))

        self.assertEquals(
            result.status_code,
            200,
            msg='Expected 200 status on finding language 1'
        )

    def test_add_one_language(self):
        """Test if a single language can be added to language resource"""
        result = self.app.post(
            self.language_endpoint,
            data=self.dummy_language
        )

        self.assertEquals(
            result.status_code,
            201,
            msg='Expected creation of dummy language'
        )

    def test_add_duplicate_language(self):
        """Test if adding the same language twice produces an error"""
        self.app.post(
            self.language_endpoint,
            data=self.dummy_language
        )

        result = self.app.post(
            self.language_endpoint,
            data=self.dummy_language
        )

        self.assertEquals(
            result.status_code,
            409,
            msg='Expected 409 status code from adding duplicate language'
        )

    def test_delete_one_language(self):
        """Test if a language can be deleted from a language resource"""
        self.app.post(
            self.language_endpoint,
            data=self.dummy_language
        )

        result = self.app.delete(
            '{}/9999'.format(self.language_endpoint)
        )
        self.assertEquals(
            result.status_code,
            202,
            msg='Expected dummy language to be deleted'
        )

    def test_delete_no_language(self):
        """test if a invalid language is deletable from languages resource"""
        result = self.app.delete('{}/44444444'.format(self.language_endpoint))

        self.assertEqual(
            result.status_code,
            404,
            msg='Expected to not find language to delete'
        )

    def test_edit_one_language(self):
        """Test if a language can be PATCHed"""
        self.app.post(
            self.language_endpoint,
            data=self.dummy_language
        )

        new_doc = json.dumps({'name': 'foobar'})

        result = self.app.patch(
            '{}/9999'.format(self.language_endpoint),
            data=new_doc
        )

        self.assertEquals(
            result.status_code,
            204,
            'Expected language to be edited'
        )
