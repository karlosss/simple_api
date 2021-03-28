from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import IntegerType, ObjectType
from simple_api.object.object import Object
from simple_api.utils import AttrDict

from simple_api.adapters.graphql.utils import build_patterns


def get(request, params, **kwargs):
    return AttrDict(number=20, number_def=5)


def get_number(request, parent_val, params, **kwargs):
    return params.get("num") or parent_val


class TestObject(Object):
    fields = {
        "number": IntegerType(parameters={"num": IntegerType(nullable=True)}, resolver=get_number),
        "number_def": IntegerType(parameters={"num": IntegerType(nullable=True, default=5)}, resolver=get_number),
    }


actions = {
    "get": Action(return_value=ObjectType(TestObject), exec_fn=get)
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
