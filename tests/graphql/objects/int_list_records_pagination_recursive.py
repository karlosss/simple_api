from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, PlainListType, ObjectType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def resolve(request, parent_val, params):
    res = parent_val["records"][params["offset"]:(params["offset"]+params["limit"])]
    return {
        "count": len(res),
        "all_records": res,
        "records": res,
    }


class IntList(Object):
    fields = {
        "count": IntegerType(),
        "all_records": PlainListType(IntegerType()),
        "records": ObjectType(
            "self",
            parameters={
                "limit": IntegerType(nullable=True, default=20),
                "offset": IntegerType(nullable=True, default=0),
            },
            resolver=Function(resolve)
        )
    }


def get(request, params):
    return {
        "count": len(params["data"]),
        "all_records": params["data"],
        "records": params["data"]
    }


actions = {
    "get": Action({"data": PlainListType(IntegerType())}, ObjectType(IntList), Function(get))
}


schema = generate(GraphQLAdapter, [IntList], actions)


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
                
                type IntList {
                  count: Int!
                  allRecords: [Int!]!
                  records(limit: Int = 20, offset: Int = 0): IntList!
                }
                
                type Query {
                  get(data: [Int!]!): IntList!
                }
                """
            )
        )

    def test_request_no_pag(self):
        resp = self.query(
            """
            query{
              get(data: [1,2,3,4,5,6,7,8,9]){
                count
                allRecords
              }
            }
            """
        )

        exp = {
          "data": {
            "get": {
              "count": 9,
              "allRecords": [
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
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_single_pag(self):
        resp = self.query(
            """
            query{
              get(data: [1,2,3,4,5,6,7,8,9]){
                count
                allRecords
                records(limit: 5, offset: 2){
                  count
                  allRecords
                }
              }
            }
            """
        )

        exp = {
          "data": {
            "get": {
              "count": 9,
              "allRecords": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9
              ],
              "records": {
                "count": 5,
                "allRecords": [
                  3,
                  4,
                  5,
                  6,
                  7
                ]
              }
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_recursive_pag(self):
        resp = self.query(
            """
            query{
              get(data: [1,2,3,4,5,6,7,8,9]){
                count
                allRecords
                records(limit: 5, offset: 2){
                  count
                  allRecords
                  records(limit: 3, offset: 1){
                    count
                    allRecords
                  }
                }
              }
            }
            """
        )

        exp = {
          "data": {
            "get": {
              "count": 9,
              "allRecords": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9
              ],
              "records": {
                "count": 5,
                "allRecords": [
                  3,
                  4,
                  5,
                  6,
                  7
                ],
                "records": {
                  "count": 3,
                  "allRecords": [
                    4,
                    5,
                    6
                  ]
                }
              }
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
