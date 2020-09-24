from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase, remove_ws


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

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
