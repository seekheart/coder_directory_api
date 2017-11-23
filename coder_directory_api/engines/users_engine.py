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
        """finds all users in the collection.

        Returns:
            users collection sorted by _id in ascending order.
        """

        return [doc for doc in self.db.find().sort('_id', pymongo.ASCENDING)]

    def find_one(self, user_id: int) -> dict:
        """finds one user in collection by _id.

        Returns:
            user document that matches _id
        """

        return self.db.find_one({'_id': user_id})

    def find_by_username(self, username: str) -> dict:
        """finds one user document by username

        Args:
            username: username to query for

        Returns:
            a user's document if it exists
        """

        return self.db.find_one({'username': username})

    def delete_one(self, user_id: int) -> bool:
        """Deletes a user document by _id

        Args:
            user_id: unique user _id number.

        Returns:
            result of delete being success or failure.
        """

        del_count = self.db.delete_one({'_id': user_id})

        if del_count.deleted_count < 1:
            return False

        return True

    def add_one(self, user: dict) -> int:
        """Adds a user document to the collection

        Args:
            user: user's document to be added to collection.

        Returns:
            user's _id if user document was successfully added.
        """

        try:
            user['_id']
        except KeyError:
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

    def edit_one(self, user_id: int, user_dict: dict) -> bool:
        """Edits a user's document

        Args:
            user_id: user's unique _id from collection.
            user_dict: user's new data in dict format

        Returns:
            Result of edit being Success or Failure.
        """

        lookup = {'_id': user_id}

        try:
            self.db.update_one(lookup, {'$set': user_dict})
            result = True
        except AttributeError as e:
            result = False

        return result
