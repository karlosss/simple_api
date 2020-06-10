from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import StringType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def echo(request, params):
    return params["string"]


class Actions(Object):
    actions = {
        "echo_non_null": Action(parameters={"string": StringType()}, return_value=StringType(), exec_fn=Function(echo)),
        "echo_default": Action(parameters={"string": StringType(nullable=True, default="default")}, return_value=StringType(), exec_fn=Function(echo)),
        "echo_null_fail": Action(parameters={"string": StringType(nullable=True)}, return_value=StringType(), exec_fn=Function(echo)),
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
