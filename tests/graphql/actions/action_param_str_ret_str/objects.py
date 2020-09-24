from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import StringType
from object.function import Function
from tests.graphql.graphql_test_utils import build_patterns


def echo(request, params):
    return params["string"]


actions = {
    "echo_non_null": Action(parameters={"string": StringType()}, return_value=StringType(), exec_fn=Function(echo)),
    "echo_default": Action(parameters={"string": StringType(nullable=True, default="default")}, return_value=StringType(), exec_fn=Function(echo)),
    "echo_null_fail": Action(parameters={"string": StringType(nullable=True)}, return_value=StringType(), exec_fn=Function(echo)),
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
