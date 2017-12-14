"""
Mongo Engine

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import pymongo
import coder_directory_api.settings as settings


class MongoEngine:
    def __init__(self, collection: str, key_manager: bool =True) -> None:
        """Constructor for mongodb connection
        Args:
            collection: name of collection to operate on.
            key_manager: sets up an automatic unique id manager, default is on.
        """

        self._host = settings.MONGO['host']
        self._port = settings.MONGO['port']
        self._db_name = settings.MONGO['db']
        self._collection = collection

        try:
            self.db = pymongo.MongoClient(self._host, self._port)[self._db_name]
            self.db = self.db.get_collection(self._collection)
        except ConnectionError:
            print('Error connecting to database!')

        if key_manager:
            try:
                self._max_id = self._set_max_id()
            except (AttributeError, ValueError):
                self._max_id = 1

    def _set_max_id(self) -> int:
        """private method to set the max id based on the collection's state

        Returns:
            Highest _id of collection.
        """
        return self.db.find().sort('_id', pymongo.DESCENDING)[0]['_id'] + 1

    def find_one(self, lookup: str) -> dict:
        pass

    def find_all(self) -> list:
        pass

    def add_one(self, data: dict) -> bool:
        pass

    def delete_one(self, lookup: str) -> None:
        pass

    def edit_one(self, lookup: str, field: dict) -> None:
        pass
