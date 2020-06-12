from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import IntegerType, PlainListType, ObjectType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


class TestObject(Object):
    fields = {
        "int1": IntegerType(),
        "int2": IntegerType(),
    }


def non_null(request, params):
    return [
        {"int1": 0, "int2": 10},
        {"int1": 1, "int2": 11},
        {"int1": 2, "int2": 12},
    ]


def null(request, params):
    return None


def list_non_null_elem_null(request, params):
    return [
        {"int1": 0, "int2": 10},
        None,
        {"int1": 2, "int2": 12},
    ]


actions = {
    "get_non_null": Action(return_value=PlainListType(ObjectType(TestObject)), exec_fn=Function(non_null)),
    "get_null": Action(return_value=PlainListType(ObjectType(TestObject, nullable=True), nullable=True), exec_fn=Function(null)),
    "get_list_null_elem_non_null": Action(return_value=PlainListType(ObjectType(TestObject), nullable=True), exec_fn=Function(null)),
    "get_list_non_null_elem_null": Action(return_value=PlainListType(ObjectType(TestObject, nullable=True)),
                                          exec_fn=Function(list_non_null_elem_null)),
}

schema = generate(GraphQLAdapter, [TestObject], actions)


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
                  getNonNull: [TestObject!]!
                  getNull: [TestObject]
                  getListNullElemNonNull: [TestObject!]
                  getListNonNullElemNull: [TestObject]!
                }
                
                type TestObject {
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
              getNonNull{
                int1
                int2
              }
            }
            """
        )

        exp = {
          "data": {
            "getNonNull": [
              {
                "int1": 0,
                "int2": 10
              },
              {
                "int1": 1,
                "int2": 11
              },
              {
                "int1": 2,
                "int2": 12
              }
            ]
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_null_elem_non_null(self):
        resp = self.query(
            """
            query{
              getListNullElemNonNull{
                int1
                int2
              }
            }
            """
        )

        exp = {
            "data": {
                "getListNullElemNonNull": None
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_non_null_elem_null(self):
        resp = self.query(
            """
            query{
              getListNonNullElemNull{
                int1
                int2
              }
            }
            """
        )

        exp = {
          "data": {
            "getListNonNullElemNull": [
              {
                "int1": 0,
                "int2": 10
              },
              None,
              {
                "int1": 2,
                "int2": 12
              }
            ]
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
