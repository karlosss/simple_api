# https://stackoverflow.com/questions/46940449/graphene-python-lists-resolve-null-for-all-fields
from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import IntegerType, StringType, PlainListType, ObjectType
from simple_api.object.object import Object

from simple_api.adapters.graphql.utils import build_patterns


def get(request, params, **kwargs):
    return [
        {'id': 39330, 'username': 'RCraig', 'email': 'WRussell@dolor.gov'},
        {'id': 39331, 'username': 'AHohmann', 'email': 'AMarina@sapien.com'}
    ]


class User(Object):
    fields = {
        "id": IntegerType(nullable=True),
        "username": StringType(nullable=True),
        "email": StringType(nullable=True),
    }


actions = {
    "users": Action(return_value=PlainListType(ObjectType(User)), exec_fn=get)
}

schema = generate(GraphQLAdapter, actions)
patterns = build_patterns("api/", schema)
