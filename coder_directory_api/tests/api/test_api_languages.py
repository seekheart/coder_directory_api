"""
Tests for Languages Resource of Coder Directory app

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from .common_test_setup import CommonApiTest
import json
import coder_directory_api.engines as engines


class LanguagesResourceTest(CommonApiTest):
    def setUp(self):
        """Setup Languages Tests"""
        super(LanguagesResourceTest, self).setUp()
        self.endpoint = '{}/languages'.format(self.base_url)
        self.engine = engines.LanguagesEngine()
        self.dummy = {
            "_id": 9999,
            "name": "test3",
            "synonyms": ["asdf", "fefe"],
            "users": [9999]
        }
        self.dummy = json.dumps(self.dummy)

    def tearDown(self):
        """Teardown Languages Tests"""
        super(LanguagesResourceTest, self).tearDown()
        try:
            self.engine.delete_one(9999)
        except AttributeError:
            pass
        self.engine = None

    def test_get_all_languages(self):
        """Test if all languages in language resource can be gotten"""
        result = self.app.get(self.endpoint)

        self.assertEquals(
            result.status_code,
            200,
            msg='Expected 200 status on languages resource'
        )

    def test_get_one_language(self):
        """Test if a single language can be gotten from language resource"""
        result = self.app.get('{}/1'.format(self.endpoint))

        self.assertEquals(
            result.status_code,
            200,
            msg='Expected 200 status on finding language 1'
        )

    def test_add_one_language(self):
        """Test if a single language can be added to language resource"""
        result = self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )

        self.assertEquals(
            result.status_code,
            201,
            msg='Expected creation of dummy language'
        )

    def test_add_duplicate_language(self):
        """Test if adding the same language twice produces an error"""
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

        self.assertEquals(
            result.status_code,
            409,
            msg='Expected 409 status code from adding duplicate language'
        )

    def test_delete_one_language(self):
        """Test if a language can be deleted from a language resource"""
        self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )

        result = self.app.delete(
            '{}/9999'.format(self.endpoint)
        )
        self.assertEquals(
            result.status_code,
            202,
            msg='Expected dummy language to be deleted'
        )

    def test_delete_no_language(self):
        """test if a invalid language is deletable from languages resource"""
        result = self.app.delete('{}/44444444'.format(self.endpoint))

        self.assertEqual(
            result.status_code,
            404,
            msg='Expected to not find language to delete'
        )

    def test_edit_one_language(self):
        """Test if a language can be PATCHed"""
        self.app.post(
            self.endpoint,
            data=self.dummy,
            content_type='application/json'
        )

        new_doc = json.dumps({'name': 'foobar'})

        result = self.app.patch(
            '{}/9999'.format(self.endpoint),
            data=new_doc,
            content_type='application/json'
        )

        self.assertEquals(
            result.status_code,
            204,
            'Expected language to be edited'
        )
