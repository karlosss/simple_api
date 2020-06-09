from graphene import ObjectType

from utils import ClassStub

_classes = {}


def get_class(cls):
    if cls not in _classes:
        _classes[cls] = ClassStub(cls.__name__, (ObjectType,)).build()
    return _classes[cls]
