from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, PlainListType, ObjectType, StringType, BooleanType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def echo(request, params):
    return params["string"]


actions = {
    "echo_safe": Action(parameters={"string": StringType()}, return_value=StringType(), exec_fn=Function(echo)),
    "echo_unsafe": Action(parameters={"string": StringType()}, return_value=StringType(), exec_fn=Function(echo), unsafe=True),
}

schema = generate(GraphQLAdapter, [], actions)


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
                  mutation: Mutation
                }
                
                type Mutation {
                  echoUnsafe(string: String!): String!
                }
                
                type Query {
                  echoSafe(string: String!): String!
                }
                """
            )
        )

    def test_request_unsafe(self):
        resp = self.query(
            """
            mutation m{
              echoUnsafe(string: "Hello")
            }
            """
        )

        exp = {
          "data": {
            "echoUnsafe": "Hello"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_safe(self):
        resp = self.query(
            """
            query{
              echoSafe(string: "Hello")
            }
            """
        )

        exp = {
            "data": {
                "echoSafe": "Hello"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
