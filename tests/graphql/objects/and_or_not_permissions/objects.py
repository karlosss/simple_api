from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import BooleanType
from simple_api.object.permissions import AllowNone, Not, AllowAll, Or, And

from tests.graphql.graphql_test_utils import build_patterns


actions = {
    "allow1": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=Not(AllowNone)),
    "allow2": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=Or(AllowAll, AllowNone)),
    "allow3": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=And(AllowAll, AllowAll)),
    "allow4": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=(AllowAll, AllowAll)),
    "allow5": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True,
                     permissions=Or(Not(AllowAll), Not(And(AllowAll, AllowNone)))),
    "deny1": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=Not(AllowAll)),
    "deny2": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=And(AllowAll, AllowNone)),
    "deny3": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=Or(AllowNone, AllowNone)),
    "deny4": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=(AllowNone, AllowNone)),
    "deny5": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True,
                    permissions=And(Not(And(AllowAll, AllowNone)), Not(AllowAll))),
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
