from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import StringType
from object.function import Function
from tests.graphql.graphql_test_utils import build_patterns


def non_null(request, params):
    return "nonNull"


def null(request, params):
    return None


actions = {
    "non_null": Action(return_value=StringType(), exec_fn=Function(non_null)),
    "null": Action(return_value=StringType(nullable=True), exec_fn=Function(null))
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
