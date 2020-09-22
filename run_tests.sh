#!/usr/bin/env bash

if [[ $# -lt 1 ]]
then
    echo "Usage: $0 VENV_NAME [PATTERN]" >&2
    exit 2
fi

cd "${0%/*}"

. "$1/bin/activate"

pattern="*.py"
if [[ -n "$2" ]]
then
    pattern=$2
fi

test_project/simple_api/manage.py test --pattern="$pattern"
