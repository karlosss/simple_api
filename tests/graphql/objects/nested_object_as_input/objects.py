from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import ObjectType, StringType, IntegerType
from simple_api.object.object import Object

from tests.graphql.graphql_test_utils import build_patterns


class Coordinates(Object):
    fields = {
        "lat": IntegerType(),
        "lng": IntegerType()
    }


class Location(Object):
    fields = {
        "name": StringType(),
        "coords": ObjectType(Coordinates)
    }


def echo(request, params, **kwargs):
    return params["loc"]


actions = {
    "echo": Action(parameters={"loc": ObjectType(Location)}, return_value=ObjectType(Location), exec_fn=echo)
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
