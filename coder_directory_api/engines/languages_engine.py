"""
Languages Engine for Coder Directory Api

Copyright (c) 2017 by Mike Tung.
MIT License, see LICENSE for details.
"""

import pymongo
from .mongo_engine import MongoEngine


class LanguagesEngine(MongoEngine):
    def __init__(self):
        """Constructor for language engine calls on Mongo Engine"""
        super(LanguagesEngine, self).__init__('languages')

    def find_all(self) -> list:
        """
        find all languages

        Returns:
            list of programming languages in languages collection sorted by _id
        """

        return [d for d in self.db.find().sort('_id', pymongo.ASCENDING)]

    def find_one(self, language_id: int) -> dict:
        """finds a single language by _id

        Args:
            language_id: unique id of language

        Returns:
            language document matching language_id
        """

        return self.db.find_one({'_id': language_id})

    def find_by_name(self, lang_name: str) -> dict:
        """finds a single language by name

        Args:
            lang_name: unique id of language

        Returns:
            language document matching name
        """

        return self.db.find_one({'name': lang_name})

    def add_one(self, lang: dict) -> int:
        """Adds a language to the languages collection

        Args:
            lang: language document to be added

        Returns:
            The unique _id for added document
        """

        try:
            lang['_id']
        except KeyError as e:
            lang['_id'] = self._max_id

        is_duplicate = self._is_duplicate_language(lang)

        if is_duplicate:
            raise AttributeError(
                'Language exists or is a synonym! {}'.format(lang)
            )

        try:
            self.db.insert_one(lang)
        except AttributeError as e:
            print('Unable to add language\n{}'.format(lang))
            print(e)

        self._max_id = self._set_max_id()
        return lang['_id']

    def delete_one(self, lang_id: int) -> bool:
        """method to delete a language from the collection by _id.

        Args:
            lang_id: unique identifier for language

        Returns:
            a bool result of deleted status
        """

        result = True

        try:
            self.db.delete_one({'_id': lang_id})
        except AttributeError as e:
            print(e)
            result = False

        return result

    def edit_one(self, lang_id: int, lang_doc: dict) -> bool:
        """
        Edits a language document with new data.

        Args:
            lang_id: unique id of language to be updated.
            lang_doc: document containing edits.

        Returns:
            Result of edit being success or failure.
        """

        lookup = {'_id': lang_id}
        try:
            self.db.update_one(lookup, {'$set': lang_doc})
            result = True
        except AttributeError as e:
            result = False
        return result

    def add_synonym(self, lang_id: int, syn: str) -> bool:
        """Method to add a synonym to a language's document

        Args:
            lang_id: unique id of language to be edited
            syn: synonym term to add

        Returns:
            status of adding synonym
        """

        lookup = {'_id': lang_id}
        is_exists = self._is_synonym(syn)

        if not is_exists:
            self.db.update_one(lookup, {'$push': {'synonyms': syn}})
            result = True
        else:
            result = False

        return result

    def delete_synonym(self, lang_id: int, syn: str) -> bool:
        """Method to delete a synonym to a language's document

        Args:
            lang_id: unique id of language to be edited
            syn: synonym term to add

        Returns:
            status of deleting synonym
        """

        lookup = {'_id': lang_id}
        is_exists = self._is_synonym(syn)

        if is_exists:
            self.db.update_one(lookup, {'$pull': {'synonyms': syn}})
            result = True
        else:
            result = False

        return result

    def _is_duplicate_language(self, lang: dict) -> bool:
        """Helper method to check if language is a duplicate or not.

        Args:
            lang: language document to validate.

        Returns:
            indicator of whether or not language is a duplicate.
        """

        is_synonym = self._is_synonym(lang['name'])
        is_exists = self.find_by_name(lang['name'])

        if is_exists or is_synonym:
            return True

        return False

    def _is_synonym(self, lang_name: str) -> bool:
        """Helper method to check for synonyms.

        Args:
            lang_name: name of language to check

        Returns:
            status of synonym
        """
        docs = self.find_all()
        for doc in docs:
            if lang_name in doc['synonyms']:
                return True

        return False


