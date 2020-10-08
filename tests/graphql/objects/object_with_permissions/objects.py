from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import StringType, ObjectType
from object.object import Object
from object.permissions import AllowNone
from tests.graphql.graphql_test_utils import build_patterns


def exec_fn(request, params, **kwargs):
    return {
        "allowed_field": None,
        "forbidden_field": None
    }


class NullableObject(Object):
    fields = {
        "allowed_field": StringType(default="allowed", nullable=True),
        "forbidden_field": StringType(default="forbidden", nullable=True, permissions=AllowNone)
    }

    actions = {
        "allowedGet": Action(return_value=ObjectType("self", nullable=True), exec_fn=exec_fn),
        "forbiddenGet": Action(return_value=ObjectType("self", nullable=True), exec_fn=exec_fn, permissions=AllowNone)
    }


class NonNullableObject(Object):
    fields = {
        "allowed_field": StringType(default="allowed"),
        "forbidden_field": StringType(default="forbidden", permissions=AllowNone)
    }

    actions = {
        "allowedGet": Action(return_value=ObjectType("self"), exec_fn=exec_fn),
        "forbiddenGet": Action(return_value=ObjectType("self"), exec_fn=exec_fn, permissions=AllowNone)
    }


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
