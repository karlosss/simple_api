#!/usr/bin/env bash

cd "${0%/*}"

# cleanup possible old runs
find test_project/simple_api/testcases ! \( -name '__init__.py' -o -name 'admin.py' -o -name 'apps.py' -o -name 'utils.py' -o -name 'views.py' \) -type f -exec rm -rf {} \;
rm -f test_project/simple_api/db.sqlite3

# copy sources into test project
cp tests/graphql/django_object_foreign_key/[!_]* test_project/simple_api/testcases

# activate virtualenv if exists
if [[ -d venv ]]
then
    . venv/bin/activate
fi

# migrate database
test_project/simple_api/manage.py makemigrations testcases
test_project/simple_api/manage.py migrate

# run tests
test_project/simple_api/manage.py test testcases.tests
