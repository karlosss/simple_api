#!/usr/bin/env bash

cd "${0%/*}"

# cleanup possible old runs
rm -rf test_project/simple_api/testcases/migrations
rm -f test_project/simple_api/testcases/models.py
rm -f test_project/simple_api/testcases/objects.py
rm -f test_project/simple_api/testcases/tests.py
rm -f test_project/simple_api/db.sqlite3

# copy sources into test project
cp tests/graphql/django_object_foreign_key/[!_]* test_project/simple_api/testcases

# migrate database
. venv/bin/activate
test_project/simple_api/manage.py makemigrations testcases
test_project/simple_api/manage.py migrate

# run tests
test_project/simple_api/manage.py test testcases.tests
