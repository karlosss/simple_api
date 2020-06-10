from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import StringType, ObjectType, IntegerType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def get(request, params):
    if "id" in params:
        return "{}.{}".format(params["id"]["int1"], params["id"]["int2"])
    return "no params passed"


class TestObject(Object):
    fields = {
        "int1": IntegerType(),
        "int2": IntegerType(),
    }


class Actions(Object):
    actions = {
        "get": Action(parameters={"id": ObjectType(TestObject)}, return_value=StringType(), exec_fn=Function(get)),
        "get_null": Action(parameters={"id": ObjectType(TestObject, nullable=True)}, return_value=StringType(), exec_fn=Function(get)),
        "get_null_default": Action(parameters={"id": ObjectType(TestObject, nullable=True, default={"int1": 10, "int2": 20})},
                                   return_value=StringType(), exec_fn=Function(get))
    }


schema = generate(GraphQLAdapter, [Actions, TestObject])


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
                  get(id: TestObjectInput!): String!
                  getNull(id: TestObjectInput): String!
                  getNullDefault(id: TestObjectInput = {int1: 10, int2: 20}): String!
                }
                
                input TestObjectInput {
                  int1: Int!
                  int2: Int!
                }
                """
            )
        )

    def test_request_non_null(self):
        resp = self.query(
            """
            query{
              get(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
          "data": {
            "get": "1.2"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_non_null_fail(self):
        resp = self.query(
            """
            query{
              get
            }
            """
        )

        self.assertResponseHasErrors(resp)

    def test_request_null_param(self):
        resp = self.query(
            """
            query{
              getNull(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
          "data": {
            "getNull": "1.2"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_no_param(self):
        resp = self.query(
            """
            query{
              getNull
            }
            """
        )

        exp = {
          "data": {
            "getNull": "no params passed"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_default_no_param(self):
        resp = self.query(
            """
            query{
              getNullDefault
            }
            """
        )

        exp = {
          "data": {
            "getNullDefault": "10.20"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_default_with_param(self):
        resp = self.query(
            """
            query{
              getNullDefault(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
          "data": {
            "getNullDefault": "1.2"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)