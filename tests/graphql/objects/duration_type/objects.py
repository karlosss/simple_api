from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import ObjectType, DurationType
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns


def echo(request, params, **kwargs):
    return params["in"]


class TestObject(Object):
    fields = {
        "duration": DurationType()
    }


actions = {
    "get": Action(return_value=DurationType(), parameters={"in": DurationType()}, exec_fn=echo),
    "getObject": Action(return_value=ObjectType(TestObject), parameters={"in": ObjectType(TestObject)}, exec_fn=echo)
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
