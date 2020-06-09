import os
from importlib import import_module

from django.urls import path
from django.conf import settings

test_root = os.path.join(settings.PROJECT_ROOT, "tests")


def register_testcases():
    out = []

    for file in os.listdir(test_root):
        f = os.path.join(test_root, file)
        if os.path.isdir(f):
            mod = import_module("tests.{}".format(file))
            if not hasattr(mod, "testcases"):
                continue
            for uri, view in mod.testcases:
                out.append(path("{}/{}".format(file, uri), view))

    return out
