from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, ObjectType
from object.function import Function
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns


def get(request, params):
    return params["default"]["number"]


def get_number(request, parent_val, params):
    return params.get("num") or parent_val


class TestObject(Object):
    fields = {
        "number": IntegerType(parameters={"num": IntegerType(nullable=True)}, resolver=Function(get_number)),
    }

    output_fields = {
        "number_def": IntegerType(parameters={"num": IntegerType(nullable=True, default=5)},
                                  resolver=Function(get_number)),
    }


actions = {
    "get": Action(parameters={"default": ObjectType(TestObject)}, return_value=ObjectType(TestObject), exec_fn=Function(get))
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
