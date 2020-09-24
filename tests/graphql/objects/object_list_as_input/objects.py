from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, PlainListType
from object.function import Function
from tests.graphql.graphql_test_utils import build_patterns


def plus_one(request, params):
    return [i+1 for i in params["list"]]


actions = {
    "plus_one": Action(parameters={"list": PlainListType(IntegerType())},
                       return_value=PlainListType(IntegerType()),
                       exec_fn=Function(plus_one)),
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
