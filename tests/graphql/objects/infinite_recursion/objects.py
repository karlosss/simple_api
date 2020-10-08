from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import ObjectType
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns


def get(request, params, **kwargs):
    return None


class TestObject(Object):
    fields = {
        "self": ObjectType("self", nullable=True)
    }


actions = {
    "get": Action(return_value=ObjectType(TestObject, nullable=True), exec_fn=get)
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
