from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import ObjectType
from simple_api.object.object import Object

from simple_api.adapters.graphql.utils import build_patterns


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
