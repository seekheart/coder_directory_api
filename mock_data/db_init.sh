#!/usr/bin/env bash
set -e

echo Dropping database...
mongo coder --eval "db.dropDatabase()"
echo Database dropped!

echo Seeding user data...
mongoimport --db coder \
--collection users \
--file mock_data/users.json \
--jsonArray
echo User data seeded!

echo Seeding language data...
mongoimport --db coder \
--collection languages \
--file mock_data/languages.json \
--jsonArray
echo Language data seeded!
