"""
Settings for Coder Directory

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import json
import os

# basic settings
HOST = os.environ.get('API_URI', '0.0.0.0')
PORT = os.environ.get('API_PORT', 3000)
SECRET = os.environ.get('API_SECRET', 'coder_directory_api/dev_settings.json')
ENV = os.environ.get('API_ENV', 'DEV')
BASE_URL = os.environ.get('API_BASE_URL', '/')
with open(SECRET, 'r') as s:
    creds = json.load(s)

MONGO = {
    'host': creds['db_host'],
    'port': creds['db_port'],
    'db': creds['db_name']
}

if ENV == 'DEV':
    DEBUG = True
    MULTITHREADING = False
elif ENV == 'PROD':
    DEBUG = False
    MULTITHREADING = True

