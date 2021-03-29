from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import ObjectType

from simple_api.adapters.graphql.utils import build_patterns

from .b import get


actions = {
    "get": Action(return_value=ObjectType("C"), exec_fn=get)
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns("api/", schema)
