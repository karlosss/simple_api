from object.datatypes import StringType, ObjectType
from object.object import Object
from .a import A


def get(request, params, **kwargs):
    return {
        "a": {
            "s1": "A"
        },
        "b": {
            "s1": "B"
        }
    }


class B(Object):
    fields = {
        "s1": StringType(),
        "s2": ObjectType("self", nullable=True)
    }


class C(Object):
    fields = {
        "a": ObjectType(A),
        "b": ObjectType("B")
    }
