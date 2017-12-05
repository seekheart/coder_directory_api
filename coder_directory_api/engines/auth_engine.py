"""
Tests for Auth Engine

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details
"""

from .mongo_engine import MongoEngine
import uuid


class AuthEngine(MongoEngine):
    def __init__(self):
        super(AuthEngine, self).__init__(
            collection='secrets',
            key_manager=False
        )

    def find_all(self) -> list:
        """
        find all auth credentials.

        Returns:
            list of auth credentials.
        """

        data = []
        for doc in self.db.find():
            doc['_id'] = str(doc['_id'])
            data.append(doc)

        return data

    def find_one(self, user: str) -> dict or bool:
        """
        find one user's credentials.

        Args:
            user: username to search auth credentials for.

        Returns:
            auth credential document matching user if exists.

        """

        data = self.db.find_one({'user': user})

        try:
            data['_id'] = str(data['_id'])
        except TypeError:
            return False

        return data

    def add_one(self, secret: dict) -> bool:
        """
        Adds auth credential to collection.

        Args:
            secret: credentials to add

        Returns:
            Boolean indicator as to whether credentials were added or not.
        """

        try:
            user = secret['user']
        except KeyError:
            return False

        exists = self.find_one(user)

        if exists:
            return False

        try:
            secret['_id'] = str(uuid.uuid4())
            self.db.insert_one(secret)
        except AttributeError:
            print('Unable to add secrets')

        return True

    def delete_one(self, user: str) -> bool:
        """
        Deletes a user's auth credential.
        Args:
            user: user whose credentials need to be deleted.

        Returns:
            Indicator as to whether auth doc was deleted or not.
        """

        result = True

        try:
            self.db.delete_one({'user': user})
        except AttributeError:
            result = False

        return result

    def edit_one(self, user: str, doc: dict) -> bool:
        """
        Edits a user's auth credential.

        Args:
            user: username to search for.
            doc: new data to update.

        Returns:
            Indicator as to whether auth doc was updated or not.
        """

        lookup = {'user': user}
        try:
            self.db.update_one(lookup, {'$set': doc})
            result = True
        except AttributeError:
            result = False

        return result

