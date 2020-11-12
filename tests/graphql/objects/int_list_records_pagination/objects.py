from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import ObjectType, PlainListType, IntegerType
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns
from utils import AttrDict


def resolve(request, parent_val, params, **kwargs):
    return parent_val[params["offset"]:(params["offset"] + params["limit"])]


class IntList(Object):
    fields = {
        "count": IntegerType(),
        "records": PlainListType(
            IntegerType(),
            parameters={
                "limit": IntegerType(nullable=True, default=20),
                "offset": IntegerType(nullable=True, default=0),
            },
            resolver=resolve
        )
    }


def get(request, params, **kwargs):
    return AttrDict(count=len(params["input"]), records=params["input"])


actions = {
    "get": Action(parameters={"input": PlainListType(IntegerType())},
                  return_value=ObjectType(IntList), exec_fn=get)
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
