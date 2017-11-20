"""
Test for Mongo Engine

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import unittest
from coder_directory_api.engines import MongoEngine

class MongoEngineTest(unittest.TestCase):
    def setUp(self):
        """Set up each test case"""
        self.engine = MongoEngine('local')

    def tearDown(self):
        """Clean up protocol after each test case"""
        self.engine = None

    def test_engine_exists(self):
        self.assertTrue(self.engine)
