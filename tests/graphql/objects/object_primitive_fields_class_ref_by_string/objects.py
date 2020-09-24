from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import ObjectType, StringType
from object.function import Function
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns
from utils import AttrDict


def non_null_only(request, params):
    return AttrDict(string_non_null="string")


def non_null_and_null(request, params):
    return AttrDict(string_non_null="string", string_null="string")


def all(request, params):
    return AttrDict(string_non_null="string", string_null="string", string_default="string")


class TestObject(Object):
    fields = {
        "string_non_null": StringType(),
        "string_null": StringType(nullable=True),
        "string_default": StringType(default="default")
    }

    actions = {
        "non_null_only": Action(return_value=ObjectType("self"), exec_fn=Function(non_null_only)),
        "non_null_and_null": Action(return_value=ObjectType("TestObject"), exec_fn=Function(non_null_and_null)),
        "all": Action(return_value=ObjectType("testcases.objects.TestObject"), exec_fn=Function(all))
    }


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
