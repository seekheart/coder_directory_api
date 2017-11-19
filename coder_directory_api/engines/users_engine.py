"""
User Engine

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details
"""

from coder_directory_api.engines import MongoEngine
import pymongo


class UsersEngine(MongoEngine):
    def __init__(self):
        super(UsersEngine, self).__init__('users')
        self._max_id = self._set_max_id()

    def _set_max_id(self):
        """private method to set the max id based on the collection's state"""
        return self.db.find().sort('_id', pymongo.DESCENDING)[0]['_id'] + 1

    def find_all(self) -> list:
        """find all method for users"""

        return [doc for doc in self.db.find()]

    def find_one(self, user_id: int) -> dict:
        """find one user by _id"""

        return self.db.find_one({'_id': user_id})

    def find_by_username(self, username: str) -> dict:
        """find one user by username

        Args:
            username: username to query for
        Returns:
            a user's document if it exists
        """

        return self.db.find_one({'username': username})

    def delete_one(self, user_id: int) -> bool:
        """Deletes a user by _id"""

        del_count = self.db.delete_one({'_id': user_id})

        if del_count.deleted_count < 1:
            return False

        return True

    def add_one(self, user: dict) -> int:
        """Adds a user"""

        if not user['_id']:
            user['_id'] = self._max_id

        user_exists = self.db.find_one({'username': user['username']})

        if user_exists:
            raise AttributeError('User {} exists!'.format(user_exists))

        try:
            self.db.insert_one(user)
        except AttributeError as e:
            print('Unable to add user {}'.format(user))
            print(e)

        self._max_id = self._set_max_id()
        return user['_id']