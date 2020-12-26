from simple_api.object.datatypes import StringType, ObjectType
from simple_api.object.object import Object


class A(Object):
    fields = {
        "s1": StringType(),
        "s2": ObjectType("self", nullable=True)
    }
