from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import PlainListType, IntegerType
from object.function import Function
from tests.graphql.graphql_test_utils import build_patterns


def non_null(request, params):
    return [i for i in range(10)]


def null(request, params):
    return None


def list_non_null_elem_null(request, params):
    return [1, 2, 3, None, None, None, 7, 8, 9]


actions = {
    "get_non_null": Action(return_value=PlainListType(IntegerType()), exec_fn=Function(non_null)),
    "get_null": Action(return_value=PlainListType(IntegerType(nullable=True), nullable=True), exec_fn=Function(null)),
    "get_list_null_elem_non_null": Action(return_value=PlainListType(IntegerType(), nullable=True), exec_fn=Function(null)),
    "get_list_non_null_elem_null": Action(return_value=PlainListType(IntegerType(nullable=True)), exec_fn=Function(list_non_null_elem_null)),
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
