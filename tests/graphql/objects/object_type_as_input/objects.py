from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import IntegerType, ObjectType, StringType
from simple_api.object.object import Object

from simple_api.adapters.graphql.utils import build_patterns


def get(request, params, **kwargs):
    if "id" in params:
        return "{}.{}".format(params["id"]["int1"], params["id"]["int2"])
    return "no params passed"


class TestObject(Object):
    fields = {
        "int1": IntegerType(),
        "int2": IntegerType(),
    }


actions = {
    "get": Action(parameters={"id": ObjectType(TestObject)}, return_value=StringType(), exec_fn=get),
    "getNull": Action(parameters={"id": ObjectType(TestObject, nullable=True)}, return_value=StringType(), exec_fn=get),
    "getNullDefault": Action(parameters={"id": ObjectType(TestObject, nullable=True, default={"int1": 10, "int2": 20})},
                             return_value=StringType(), exec_fn=get)
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
