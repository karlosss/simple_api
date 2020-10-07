from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, ObjectType
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns


class TestObject(Object):
    fields = {
        "field": IntegerType(),
        "nullable_if_input_field": IntegerType(nullable_if_input=True),
    }
    input_fields = {
        "only_input_field": IntegerType()
    }
    output_fields = {
        "only_output_field": IntegerType(nullable=True)
    }


def get(request, params):
    return {
        "field": 1,
        "nullable_if_input_field": 2
    }


actions = {
    "get": Action({"in": ObjectType(TestObject)}, ObjectType(TestObject), get)
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
