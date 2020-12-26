from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import ObjectType, PlainListType, IntegerType
from simple_api.object.object import Object
from simple_api.utils import AttrDict

from tests.graphql.graphql_test_utils import build_patterns


def resolve(request, parent_val, params, **kwargs):
    res = parent_val[params["offset"]:(params["offset"]+params["limit"])]
    return AttrDict(count=len(res), all_records=res, records=res)


class IntList(Object):
    fields = {
        "count": IntegerType(),
        "all_records": PlainListType(IntegerType()),
        "records": ObjectType(
            "self",
            parameters={
                "limit": IntegerType(nullable=True, default=20),
                "offset": IntegerType(nullable=True, default=0),
            },
            resolver=resolve
        )
    }


def get(request, params, **kwargs):
    return AttrDict(count=len(params["input"]), all_records=params["input"], records=params["input"])


actions = {
    "get": Action(parameters={"input": PlainListType(IntegerType())}, return_value=ObjectType(IntList), exec_fn=get)
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
