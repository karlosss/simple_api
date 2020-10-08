from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import StringType
from tests.graphql.graphql_test_utils import build_patterns


def echo(request, params, **kwargs):
    return params["string"]


actions = {
    "echo_safe": Action(parameters={"string": StringType()}, return_value=StringType(), exec_fn=echo),
    "echo_unsafe": Action(parameters={"string": StringType()}, return_value=StringType(), exec_fn=echo, mutation=True),
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
