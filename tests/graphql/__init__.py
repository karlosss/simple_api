import os
from importlib import import_module

from graphene_django.views import GraphQLView


test_root = os.path.dirname(os.path.abspath(__file__))


def allsplit_path(path):
    head, tail = os.path.split(path)
    if not head:
        return [tail]
    return allsplit_path(head) + [tail]


def _autodiscover_testcases(root, testcases):

    for file in os.listdir(root):
        f = os.path.join(root, file)

        if os.path.isdir(f):
            _autodiscover_testcases(f, testcases)
            continue

        if f.endswith(".py") and f != "__init__.py":
            relpath = os.path.relpath(root, test_root)
            if relpath == ".":
                relpath = []
            else:
                relpath = allsplit_path(relpath)

            mod_name = file[:-3]
            if relpath:
                mod_name = "{}.{}".format(".".join(relpath), mod_name)

            mod = import_module("tests.graphql.{}".format(mod_name))

            if 'schema' not in dir(mod):
                continue
            testcases.append((mod_name, mod.schema))

    return testcases


def autodiscover_testcases():
    testcases = []

    _autodiscover_testcases(test_root, testcases)

    out = []
    for name, schema in testcases:
        out.append((name.replace(".", "/") + "/", GraphQLView.as_view(graphiql=True, schema=schema)))
    return out


testcases = autodiscover_testcases()
