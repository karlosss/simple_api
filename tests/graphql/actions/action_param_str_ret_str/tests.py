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
                }
                
                type Query {
                  echo_non_null(string: String!): String!
                  echo_default(string: String = "default"): String!
                  echo_null_fail(string: String): String!
                }
                """
            )
        )

    def test_request_echo_non_null(self):
        resp = self.query(
            """
            query{
              echo_non_null(string: "hello")
            }
            """
        )

        exp = {
          "data": {
            "echo_non_null": "hello"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_echo_default_with_param(self):
        resp = self.query(
            """
            query{
              echo_default(string: "hello")
            }
            """
        )

        exp = {
          "data": {
            "echo_default": "hello"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_echo_default_no_param(self):
        resp = self.query(
            """
            query{
              echo_default
            }
            """
        )

        exp = {
          "data": {
            "echo_default": "default"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_echo_null_fail(self):
        resp = self.query(
            """
            query{
              echo_null_fail
            }
            """
        )

        self.assertResponseHasErrors(resp)
