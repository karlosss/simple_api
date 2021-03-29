from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import IntegerType, PlainListType

from simple_api.adapters.graphql.utils import build_patterns


def plus_one(request, params, **kwargs):
    return [i+1 for i in params["list"]]


actions = {
    "plusOne": Action(parameters={"list": PlainListType(IntegerType())},
                      return_value=PlainListType(IntegerType()),
                      exec_fn=plus_one),
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns("api/", schema)
