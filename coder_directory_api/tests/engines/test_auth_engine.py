"""
Tests for Auth Engine

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details
"""

import unittest
import datetime
from coder_directory_api import auth_engine


class AuthEngineTest(unittest.TestCase):
    def setUp(self):
        """Setup testing environment for each test case"""
        self.engine = auth_engine.AuthEngine()
        self.dummy_creds = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            'accessToken': 'asdf',
            'refreshToken': 'efoianeopf',
            'user': 'dummy',
        }
        try:
            self.engine.delete_one('dummy')
        except AttributeError:
            pass

    def tearDown(self):
        """Clean up protocol after each test case"""
        try:
            self.engine.delete_one('dummy')
        except AttributeError:
            pass
        self.engine = None

    def test_find_all(self):
        """Test if engine can return entire auth collection"""
        result = self.engine.find_all()
        self.assertTrue(result, msg='Expected to find all auth docs')

    def test_find_one(self):
        """Test if engine can find a single auth doc given a username"""
        result = self.engine.find_one('seekheart')
        self.assertTrue(
            result,
            msg='Expected to find a single auth document'
        )

        self.assertEqual(
            result['user'],
            'seekheart',
            msg='Expected user to be seekheart'
        )

    def test_find_one_none(self):
        """Test if engine can return nothing if no user found"""
        result = self.engine.find_one('abc')
        self.assertFalse(result, msg='Expected no results')

    def test_add_one(self):
        """Test if engine can add auth credentials"""
        result = self.engine.add_one(self.dummy_creds)
        self.assertTrue(result, msg='Expected creds to be added')

    def test_delete_one(self):
        """Test if engine can delete auth credentials by username"""
        self.engine.add_one(self.dummy_creds)
        result = self.engine.delete_one('dummy')
        self.assertTrue(
            result,
            msg='Expected creds to be deleted'
        )

    def test_edit_one(self):
        """Test if engine can edit credentials"""
        new_creds = {
            'exp': 1000,
            'accessToken': 'acs',
            'refreshToken': 'nope'
        }
        self.engine.add_one(self.dummy_creds)
        result = self.engine.edit_one(user='dummy', doc=new_creds)

        self.assertTrue(
            result,
            msg='expected update to return True'
        )

