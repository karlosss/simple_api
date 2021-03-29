from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import IntegerType, PlainListType, ObjectType
from simple_api.object.object import Object

from simple_api.adapters.graphql.utils import build_patterns


class TestObject(Object):
    fields = {
        "int1": IntegerType(),
        "int2": IntegerType(),
    }


def non_null(request, params, **kwargs):
    return [
        {"int1": 0, "int2": 10},
        {"int1": 1, "int2": 11},
        {"int1": 2, "int2": 12},
    ]


def null(request, params, **kwargs):
    return None


def list_non_null_elem_null(request, params, **kwargs):
    return [
        {"int1": 0, "int2": 10},
        None,
        {"int1": 2, "int2": 12},
    ]


actions = {
    "getNonNull": Action(return_value=PlainListType(ObjectType(TestObject)), exec_fn=non_null),
    "getNull": Action(return_value=PlainListType(ObjectType(TestObject, nullable=True), nullable=True), exec_fn=null),
    "getListNullElemNonNull": Action(return_value=PlainListType(ObjectType(TestObject), nullable=True), exec_fn=null),
    "getListNonNullElemNull": Action(return_value=PlainListType(ObjectType(TestObject, nullable=True)),
                                     exec_fn=list_non_null_elem_null),
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns("api/", schema)
