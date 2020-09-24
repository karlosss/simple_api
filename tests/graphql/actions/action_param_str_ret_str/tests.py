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
                  echoNonNull(string: String!): String!
                  echoDefault(string: String = "default"): String!
                  echoNullFail(string: String): String!
                }
                """
            )
        )

    def test_request_echo_non_null(self):
        resp = self.query(
            """
            query{
              echoNonNull(string: "hello")
            }
            """
        )

        exp = {
          "data": {
            "echoNonNull": "hello"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_echo_default_with_param(self):
        resp = self.query(
            """
            query{
              echoDefault(string: "hello")
            }
            """
        )

        exp = {
          "data": {
            "echoDefault": "hello"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_echo_default_no_param(self):
        resp = self.query(
            """
            query{
              echoDefault
            }
            """
        )

        exp = {
          "data": {
            "echoDefault": "default"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_echo_null_fail(self):
        resp = self.query(
            """
            query{
              echoNullFail
            }
            """
        )

        self.assertResponseHasErrors(resp)
