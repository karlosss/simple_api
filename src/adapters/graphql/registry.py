import graphene

from adapters.graphql.constants import INPUT_CLASS_SUFFIX
from utils import ClassStub, AttrDict

_classes = {}


def get_class(cls):
    assert not cls.__name__.endswith(INPUT_CLASS_SUFFIX), \
        "`{}`: An object name cannot end with `Input`.".format(cls.__name__)

    cls_str = "{}.{}".format(cls.__module__, cls.__name__)
    if cls_str not in _classes:
        _classes[cls_str] = AttrDict(
            output=ClassStub(cls.__name__, (graphene.ObjectType,)).build(),
            input=ClassStub("{}{}".format(cls.__name__, INPUT_CLASS_SUFFIX), (graphene.InputObjectType,)).build(),
        )
    return _classes[cls_str]
