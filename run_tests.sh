#!/usr/bin/env bash

shopt -s nullglob

TEST_DIRS=(
    tests/graphql/actions
    tests/graphql/django_objects
    tests/graphql/objects
    tests/graphql/stack_overflow
    tests/graphql/readme_forum
)

cd "${0%/*}"

# testcases filtering by regex
if [[ -n "$1" ]]
then
    filter=$1
else
    filter="*"
fi

# activate virtualenv if exists
if [[ -d venv ]]
then
    . venv/bin/activate
fi

for dir in "${TEST_DIRS[@]}"
do
    for tc in "$dir"/[!_]*
    do
        # ignore if the testcase does not match the filter
        if ! grep -E "$filter" <<< "$tc" &>/dev/null
        then
            continue
        fi
        echo "Running $dir/$tc"

        # cleanup possible old runs
        find test_project/simple_api/testcases ! \( -name '__init__.py' -o -name 'admin.py' -o -name 'apps.py' -o -name 'utils.py' -o -name 'views.py' \) -type f -exec rm -rf {} \;
        rm -f test_project/simple_api/db.sqlite3

        # copy sources into test project
        cp "$tc"/[!_]* test_project/simple_api/testcases

        # migrate database
        test_project/simple_api/manage.py makemigrations testcases &>/dev/null
        test_project/simple_api/manage.py migrate &>/dev/null

        # run tests
        if ! test_project/simple_api/manage.py test testcases.tests
        then
            echo "$tc failed!" >&2
            exit 1
        fi
    done
done
