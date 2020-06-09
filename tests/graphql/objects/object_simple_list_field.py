from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import IntegerType, PlainListType
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def non_null(*args, **kwargs):
    return [i for i in range(10)]


def null(*args, **kwargs):
    return None


def list_non_null_elem_null(*args, **kwargs):
    return [1, 2, 3, None, None, None, 7, 8, 9]


class Actions(Object):
    actions = {
        "get_non_null": Action(return_value=PlainListType(IntegerType()), exec_fn=non_null),
        "get_null": Action(return_value=PlainListType(IntegerType(nullable=True), nullable=True), exec_fn=null),
        "get_list_null_elem_non_null": Action(return_value=PlainListType(IntegerType(), nullable=True), exec_fn=null),
        "get_list_non_null_elem_null": Action(return_value=PlainListType(IntegerType(nullable=True)), exec_fn=list_non_null_elem_null),
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
                  getNonNull: [Int!]!
                  getNull: [Int]
                  getListNullElemNonNull: [Int!]
                  getListNonNullElemNull: [Int]!
                }
                """
            )
        )

    def test_request_non_null(self):
        resp = self.query(
            """
            query{
              getNonNull
            }
            """
        )

        exp = {
          "data": {
            "getNonNull": [
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9
            ]
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_null_elem_non_null(self):
        resp = self.query(
            """
            query{
              getListNullElemNonNull
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
              getListNonNullElemNull
            }
            """
        )

        exp = {
          "data": {
            "getListNonNullElemNull": [
              1,
              2,
              3,
              None,
              None,
              None,
              7,
              8,
              9
            ]
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
