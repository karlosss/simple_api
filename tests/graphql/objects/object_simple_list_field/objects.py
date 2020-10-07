from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import PlainListType, IntegerType
from tests.graphql.graphql_test_utils import build_patterns


def non_null(request, params):
    return [i for i in range(10)]


def null(request, params):
    return None


def list_non_null_elem_null(request, params):
    return [1, 2, 3, None, None, None, 7, 8, 9]


actions = {
    "getNonNull": Action(return_value=PlainListType(IntegerType()), exec_fn=non_null),
    "getNull": Action(return_value=PlainListType(IntegerType(nullable=True), nullable=True), exec_fn=null),
    "getListNullElemNonNull": Action(return_value=PlainListType(IntegerType(), nullable=True), exec_fn=null),
    "getListNonNullElemNull": Action(return_value=PlainListType(IntegerType(nullable=True)),
                                     exec_fn=list_non_null_elem_null),
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
