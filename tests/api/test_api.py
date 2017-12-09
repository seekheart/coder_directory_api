"""
Tests for Coder Directory app

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""
import unittest
from .common_test_setup import CommonApiTest


class AppTest(CommonApiTest):

    def setUp(self):
        """Setup base api tests"""
        super(AppTest, self).setUp()

    def tearDown(self):
        """Teardown base api tests"""
        super(AppTest, self).tearDown()

    def test_base_url(self):
        """test to make sure home endpoint exists"""
        result = self.app.get(self.base_url)
        self.assertEquals(
            result.status_code,
            200,
            msg='expected home url to give 200 status')
