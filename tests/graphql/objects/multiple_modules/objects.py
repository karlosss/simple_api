from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import ObjectType
from object.function import Function
from tests.graphql.graphql_test_utils import build_patterns
from .b import get


actions = {
    "get": Action(return_value=ObjectType("C"), exec_fn=Function(get))
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
