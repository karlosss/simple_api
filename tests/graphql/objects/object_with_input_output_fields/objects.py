from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import IntegerType, ObjectType
from simple_api.object.object import Object

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


def get(request, params, **kwargs):
    return {
        "field": 1,
        "nullable_if_input_field": 2
    }


actions = {
    "get": Action(parameters={"in": ObjectType(TestObject)}, return_value=ObjectType(TestObject), exec_fn=get)
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
