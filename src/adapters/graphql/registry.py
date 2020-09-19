import graphene

from adapters.graphql.constants import INPUT_CLASS_SUFFIX
from utils import ClassStub

_input_classes = {}
_output_classes = {}


def get_class(cls, input=False):
    assert not cls.__name__.endswith(INPUT_CLASS_SUFFIX), \
        "`{}`: An object name cannot end with `{}`.".format(cls.__name__, INPUT_CLASS_SUFFIX)

    cls_str = "{}.{}".format(cls.__module__, cls.__name__)

    if input:
        if cls_str not in _input_classes:
            _input_classes[cls_str] = {"cls": ClassStub("{}{}".format(cls.__name__, INPUT_CLASS_SUFFIX),
                                                        (graphene.InputObjectType,)).build(),
                                       "used": False}
        else:
            _input_classes[cls_str]["used"] = True
        return _input_classes[cls_str]["cls"]
    else:
        if cls_str not in _output_classes:
            _output_classes[cls_str] = {"cls": ClassStub(cls.__name__, (graphene.ObjectType,)).build(),
                                        "used": False}
        else:
            _output_classes[cls_str]["used"] = True
        return _output_classes[cls_str]["cls"]


def check_classes_for_fields():
    for name, cls in _input_classes.items():
        assert cls["cls"]._meta.fields or not cls["used"], \
            "Object `{}` is used as input, but does not contain any input fields.".format(name)

    for name, cls in _output_classes.items():
        assert cls["cls"]._meta.fields or not cls["used"], \
            "Object `{}` is used as output, but does not contain any output fields.".format(name)
