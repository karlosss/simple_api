import os

from simple_api.settings import PROJECT_ROOT


def get_graphql_url(file):
    return "/" + os.path.relpath(os.path.abspath(file), os.path.join(PROJECT_ROOT, "tests"))[:-3] + "/"


def remove_ws(s):
    return " ".join(s.split())
