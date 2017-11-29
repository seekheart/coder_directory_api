"""
Google OAuth Custom Backend

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

from flask_dance.consumer.backend import BaseBackend
from coder_directory_api.engines import UsersEngine

class GoogleAuthEngine(BaseBackend):
    def __init__(self):
        super(GoogleAuthEngine, self).__init__()
        self.user_engine = UsersEngine()

    def get(self, blueprint):
        return self.user_engine.find_all()[0]

    def delete(self, blueprint):
        super().delete(blueprint)

    def set(self, blueprint, token):
        print(blueprint)
        print(token)
        super().set(blueprint, token)
