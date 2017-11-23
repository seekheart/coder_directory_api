"""
Mongo Engine

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import pymongo
import coder_directory_api.settings as settings


class MongoEngine:
    def __init__(self, collection: str) -> None:
        """Constructor for mongodb connection
        Args:
            collection_name: name of collection to operate on
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
