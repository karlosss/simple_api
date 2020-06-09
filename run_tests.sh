#!/usr/bin/env bash

if [[ $# -ne 1 ]]
then
    echo "Usage: $0 VENV_NAME" >&2
    exit 2
fi

cd "${0%/*}"

. "$1/bin/activate"

test_project/simple_api/manage.py test --pattern="*.py"
