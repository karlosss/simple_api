import graphene

from utils import ClassStub, AttrDict

_classes = {}


def get_class(cls):
    if cls not in _classes:
        _classes[cls] = AttrDict(
            output=ClassStub(cls.__name__, (graphene.ObjectType,)).build(),
            input=ClassStub(cls.__name__, (graphene.InputObjectType,)).build(),
        )

    return _classes[cls]
