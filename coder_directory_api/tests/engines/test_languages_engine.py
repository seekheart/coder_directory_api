"""
Test for Languages Engine

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""


import unittest
from coder_directory_api.engines import LanguagesEngine

class TestLanguagesEngine(unittest.TestCase):
    def setUp(self):
        """Setup testing environment for each test case"""
        self.engine = LanguagesEngine()
        self.dummy_language = {
            '_id': 9999,
            'name': 'test',
            'synonyms': ['test1', 'test2'],
            'users': [1, 2]
        }

        try:
            self.engine.delete_one(self.dummy_language['_id'])
        except AttributeError:
            pass

    def tearDown(self):
        """Cleans up each test case after execution"""
        self.engine = None

    def test_find_all(self):
        """Tests if engine can find all languages in collection"""
        result = self.engine.find_all()

        self.assertTrue(
            result,
            msg='expected language engine to return results')
        self.assertNotEquals(
            len(result),
            0,
            msg='Expected non-zero results'
        )

    def test_find_one(self):
        """Tests if engine can find one language from a collection by _id"""
        result = self.engine.find_one(1)
        self.assertTrue(
            result,
            msg='Expected language engine to return results'
        )

        self.assertEquals(
            result['_id'],
            1,
            msg='Expected _id to be 1'
        )

    def test_find_by_name(self):
        """Tests if engine can find a language by name"""
        result = self.engine.find_by_name('java')

        self.assertTrue(
            result,
            msg='Expected language engine to return results'
        )

        self.assertEquals(
            result['name'],
            'java',
            msg='Expected language name returned to be java'
        )

    def test_add_one(self):
        """Tests if engine can add a new language to collection"""

        result = self.engine.add_one(self.dummy_language)

        self.assertTrue(
            result,
            msg='Expected language engine to return results'
        )

        self.assertEquals(
            result,
            9999,
            msg='expected result id to be 9999'
        )

    def test_delete_one(self):
        """Tests if engine can delete a language from collection"""

        self.engine.add_one(self.dummy_language)
        result = self.engine.delete_one(9999)

        self.assertTrue(
            result,
            msg='Expected language engine to return results'
        )

        self.assertFalse(
            self.engine.find_one(9999),
            msg='Expected dummy language to be deleted'
        )

    def test_edit_one(self):
        """Test if engine can edit a language doc"""
        self.engine.add_one(self.dummy_language)
        result = self.engine.edit_one(9999, {'name': 'test2'})

        self.assertTrue(
            result,
            msg='Expected language engine to return results'
        )

        updated_doc = self.engine.find_by_name('test2')
        self.assertTrue(
            updated_doc,
            msg='Expected updated doc'
        )
        self.assertEquals(
            updated_doc['name'],
            'test2',
            msg='expected language name to have been updated'
        )

    def test_add_synonym(self):
        """Tests method to add synonym to a language"""

        self.engine.add_one(self.dummy_language)
        result = self.engine.add_synonym(
            self.dummy_language['_id'],
            'bob'
        )

        self.assertTrue(result, msg='Expected synonym to be added')

        doc = self.engine.find_one(9999)
        self.assertEquals(
            len(doc['synonyms']),
            3,
            msg='expected synonym to be added to document'
        )

        self.assertIn(
            'bob',
            doc['synonyms'],
            msg='Expected bob to be in synonyms'
        )

    def test_is_duplicate_language(self):
        """Tests helper method for checking if a language is a duplicate"""
        result = self.engine._is_duplicate_language({'name': 'python'})

        self.assertTrue(result, msg='Expected duplicate language to be caught')

    def test_is_not_duplicate_language(self):
        """Tests helper method for checking if a language is a duplicate"""
        result = self.engine._is_duplicate_language({'name': 'p'})

        self.assertFalse(
            result,
            msg='Expected no duplicate languages to be caught')

    def test_is_synonym(self):
        """Tests helper method for checking if a language is a synonym"""

        result = self.engine._is_synonym('python')
        self.assertTrue(result, 'Expected synonym to be found')

    def test_is_not_synonym(self):
        """Tests helper method for checking if a language is a synonym"""

        result = self.engine._is_synonym('p')
        self.assertFalse(result, 'Expected synonym to not be found')