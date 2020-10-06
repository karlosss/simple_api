from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, ObjectType
from object.function import Function
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns
from utils import AttrDict


def get(request, params):
    return AttrDict(number=20, number_def=5)


def get_number(request, parent_val, params, **kwargs):
    return params.get("num") or parent_val


class TestObject(Object):
    fields = {
        "number": IntegerType(parameters={"num": IntegerType(nullable=True)}, resolver=Function(get_number)),
        "number_def": IntegerType(parameters={"num": IntegerType(nullable=True, default=5)}, resolver=Function(get_number)),
    }


actions = {
    "get": Action(return_value=ObjectType(TestObject), exec_fn=Function(get))
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
