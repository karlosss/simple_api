import graphene

from utils import ClassStub, AttrDict

_classes = {}


def get_class(cls):
    cls_str = "{}.{}".format(cls.__module__, cls.__name__)
    if cls_str not in _classes:
        _classes[cls_str] = AttrDict(
            output=ClassStub(cls.__name__, (graphene.ObjectType,)).build(),
            input=ClassStub("{}Input".format(cls.__name__), (graphene.InputObjectType,)).build(),
        )
    return _classes[cls_str]
