from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import IntegerType, PlainListType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def plus_one(request, params):
    return [i+1 for i in params["list"]]


class Actions(Object):
    actions = {
        "plus_one": Action(parameters={"list": PlainListType(IntegerType())},
                           return_value=PlainListType(IntegerType()),
                           exec_fn=Function(plus_one)),
    }


schema = generate(GraphQLAdapter, [Actions])


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
                  plusOne(list: [Int!]!): [Int!]!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              plusOne(list: [1, 2, 3, 4])
            }
            """
        )

        exp = {
          "data": {
            "plusOne": [
              2,
              3,
              4,
              5
            ]
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
