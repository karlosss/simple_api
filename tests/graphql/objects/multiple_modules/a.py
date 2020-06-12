from object.datatypes import StringType, ObjectType
from object.object import Object


class A(Object):
    fields = {
        "s1": StringType(),
        "s2": ObjectType("self", nullable=True)
    }
