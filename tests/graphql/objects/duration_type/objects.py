from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import ObjectType, DurationType
from simple_api.object.object import Object

from simple_api.adapters.graphql.utils import build_patterns


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
patterns = build_patterns("api/", schema)
