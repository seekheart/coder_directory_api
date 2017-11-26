"""
Common Setup for all Api Tests

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import coder_directory_api
import unittest


class CommonApiTest(unittest.TestCase):
    """Common Api Test Case for testing api behavior"""
    def setUp(self):
        """Common setup for api tests"""
        app = coder_directory_api.create_app()
        app.config['TESTING'] = True
        app.config['WTF_CRSF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = coder_directory_api.settings.BASE_URL

    def tearDown(self):
        """Common teardown methods for api tests"""
        self.app = None
