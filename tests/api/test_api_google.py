"""
Tests for Google Resource

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from .common_test_setup import CommonApiTest
import json
from coder_directory_api.engines import AuthEngine

class GoogleResourceTest(CommonApiTest):
    def setUp(self):
        """Setup Google Tests"""
        super(GoogleResourceTest, self).setUp()
        self.endpoint = '{}/google'.format(self.base_url)
        self.engine = AuthEngine()

    def tearDown(self):
        """Teardown method for Google Tests"""
        super(GoogleResourceTest, self).tearDown()

    def test_redirect(self):
        """Test google oauth sign in redirect"""
        result = self.app.get(self.endpoint)
        self.assertEqual(result.status_code,
                         302,
                         msg='Expected 301 redirect to Google')