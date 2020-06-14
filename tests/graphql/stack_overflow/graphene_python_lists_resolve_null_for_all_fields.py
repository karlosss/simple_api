# https://stackoverflow.com/questions/46940449/graphene-python-lists-resolve-null-for-all-fields
from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, StringType, PlainListType, ObjectType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


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
    "users": Action(return_value=PlainListType(ObjectType(User)), exec_fn=Function(get))
}

schema = generate(GraphQLAdapter, [User], actions)


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = get_graphql_url(__file__)

    def test_schema(self):
        self.assertEqual(
            remove_ws(str(self.GRAPHQL_SCHEMA)),
            remove_ws(
                """
                schema {
                  query: Query
                }
                
                type Query {
                  users: [User!]!
                }
                
                type User {
                  id: Int
                  username: String
                  email: String
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              users{
                id
                username
                email
              }
            }
            """
        )

        exp = {
          "data": {
            "users": [
              {
                "id": 39330,
                "username": "RCraig",
                "email": "WRussell@dolor.gov"
              },
              {
                "id": 39331,
                "username": "AHohmann",
                "email": "AMarina@sapien.com"
              }
            ]
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
