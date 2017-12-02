"""
Tests for User Engine

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details
"""

import unittest
from coder_directory_api import users_engine


class TestUsersEngine(unittest.TestCase):
    def setUp(self):
        """Setup testing environment for each test case"""
        self.engine = users_engine.UsersEngine()
        self.dummy_user = {
            '_id': 99999,
            'username': 'dummy',
            'languages': [1, 2, 3],
            'profile': {
                'bio': 'I\'m pretty',
                'learning': 'how to be r3alz'
            }
        }
        try:
            self.engine.delete_one(99999)
        except AttributeError as e:
            pass

    def tearDown(self):
        """Clean up protocol after each test case"""
        try:
            self.engine.delete_one(99999)
        except AttributeError as e:
            pass
        self.engine = None

    def test_find_all(self):
        """Test if engine can return entire user collection"""
        result = self.engine.find_all()
        self.assertTrue(
            result,
            msg='expected find all to find all users')

    def test_find_one_user(self):
        """Test if engine can return one user by _id"""
        result = self.engine.find_one(1)
        self.assertTrue(
            result,
            msg='expected to find user 1')
        self.assertEquals(
            result['username'],
            'test1',
            msg='expected username test1')

    def test_find_by_username(self):
        """Test if engine can return one user by username"""
        result = self.engine.find_by_username('test1')
        self.assertTrue(
            result,
            msg='expected to find test1 as user'
        )

    def test_find_by_username_fail(self):
        """Test if engine return nothing when username does not exist"""
        result = self.engine.find_by_username('asdf')
        self.assertFalse(
            result,
            msg='expected to not find a user'
        )

    def test_add_one_user(self):
        """Test if engine can add a user to collection and increment _id"""
        result = self.engine.add_one(self.dummy_user)
        self.assertEquals(result, 99999, 'Expected dummy user to be added')
        self.assertEquals(self.engine._max_id, 100000,
                          'Expected max id to raise')

    def test_add_existing_user(self):
        """Test if engine can recognize an already existing user and bounce"""
        self.engine.add_one(self.dummy_user)
        with self.assertRaises(AttributeError, msg='expected error raised'):
            self.engine.add_one(
                self.dummy_user)

    def test_delete_one_user(self):
        """Test if engine can delete a user by _id from collection"""
        self.engine.add_one(self.dummy_user)
        result = self.engine.delete_one(self.dummy_user['_id'])

        self.assertTrue(result, msg='expected engine to respond with results')
        self.assertFalse(
            self.engine.find_one(self.dummy_user['_id']),
            msg='Expected dummy user to not exist'
        )

    def test_delete_one_user_fail(self):
        """Test if engine can fail at deleting a non existent user"""
        result = self.engine.delete_one(99999999)
        self.assertFalse(
            result,
            msg='expected non-existent user to raise error')
