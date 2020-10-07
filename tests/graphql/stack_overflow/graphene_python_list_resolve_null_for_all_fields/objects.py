# https://stackoverflow.com/questions/46940449/graphene-python-lists-resolve-null-for-all-fields
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, StringType, PlainListType, ObjectType
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns


def get(request, params):
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
patterns = build_patterns(schema)
