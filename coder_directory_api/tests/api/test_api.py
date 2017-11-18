"""
Tests for Coder Directory api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""
import unittest
from coder_directory_api import api


class ApiTest(unittest.TestCase):
    def setUp(self):
        """Sets up api prior to performing each test"""
        api.config['TESTING'] = True
        api.config['WTF_CRSF_ENABLED'] = False
        self.api = api.test_client()

    def tearDown(self):
        """Clean up protocol for api after each test"""
        self.app = None

    def test_home(self):
        result = self.api.get('/')
        self.assertEquals(result.status_code,
                          200,
                          msg='Expected 200 status code')
