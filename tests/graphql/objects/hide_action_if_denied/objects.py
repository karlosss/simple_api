from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import StringType, ObjectType, BooleanType
from object.object import Object
from object.permissions import AllowNone, Not, AllowAll, Or, And
from tests.graphql.graphql_test_utils import build_patterns


actions = {
    "allow": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=AllowAll),
    "deny": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=AllowNone),
    "hide": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=AllowNone,
                   hide_if_denied=True),
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
