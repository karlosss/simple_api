from datetime import timedelta

from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import BooleanType
from simple_api.object.permissions import AllowNone, AllowAll

from simple_api.adapters.graphql.utils import build_patterns


actions = {
    "allow": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=AllowAll,
                    retry_in=timedelta(hours=1)),
    "deny": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=AllowNone,
                   retry_in=timedelta(days=3, seconds=10)),
    "hide": Action(return_value=BooleanType(), exec_fn=lambda **kwargs: True, permissions=AllowNone,
                   hide_if_denied=True),
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns("api/", schema)
