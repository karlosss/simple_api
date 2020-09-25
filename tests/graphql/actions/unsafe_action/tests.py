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
                  echo_unsafe(string: String!): String!
                }

                type Query {
                  echo_safe(string: String!): String!
                }
                """
            )
        )

    def test_request_unsafe(self):
        resp = self.query(
            """
            mutation m{
              echo_unsafe(string: "Hello")
            }
            """
        )

        exp = {
            "data": {
                "echo_unsafe": "Hello"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_safe(self):
        resp = self.query(
            """
            query{
              echo_safe(string: "Hello")
            }
            """
        )

        exp = {
            "data": {
                "echo_safe": "Hello"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
