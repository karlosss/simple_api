from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, PlainListType, ObjectType
from object.function import Function
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns


class TestObject(Object):
    fields = {
        "int1": IntegerType(),
        "int2": IntegerType(),
    }


def non_null(request, params):
    return [
        {"int1": 0, "int2": 10},
        {"int1": 1, "int2": 11},
        {"int1": 2, "int2": 12},
    ]


def null(request, params):
    return None


def list_non_null_elem_null(request, params):
    return [
        {"int1": 0, "int2": 10},
        None,
        {"int1": 2, "int2": 12},
    ]


actions = {
    "get_non_null": Action(return_value=PlainListType(ObjectType(TestObject)), exec_fn=Function(non_null)),
    "get_null": Action(return_value=PlainListType(ObjectType(TestObject, nullable=True), nullable=True), exec_fn=Function(null)),
    "get_list_null_elem_non_null": Action(return_value=PlainListType(ObjectType(TestObject), nullable=True), exec_fn=Function(null)),
    "get_list_non_null_elem_null": Action(return_value=PlainListType(ObjectType(TestObject, nullable=True)),
                                          exec_fn=Function(list_non_null_elem_null)),
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
