from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import ObjectType, StringType
from simple_api.object.object import Object
from simple_api.utils import AttrDict

from tests.graphql.graphql_test_utils import build_patterns


def non_null_only(request, params, **kwargs):
    return AttrDict(string_non_null="string")


def non_null_and_null(request, params, **kwargs):
    return AttrDict(string_non_null="string", string_null="string")


def all(request, params, **kwargs):
    return AttrDict(string_non_null="string", string_null="string", string_default="string")


class TestObject(Object):
    fields = {
        "string_non_null": StringType(),
        "string_null": StringType(nullable=True),
        "string_default": StringType(default="default")
    }

    actions = {
        "nonNullOnly": Action(return_value=ObjectType("self"), exec_fn=non_null_only),
        "nonNullAndNull": Action(return_value=ObjectType("TestObject"), exec_fn=non_null_and_null),
        "all": Action(return_value=ObjectType("testcases.objects.TestObject"), exec_fn=all)
    }


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
