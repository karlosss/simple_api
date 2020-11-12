from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase, remove_ws


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    REF_GRAPHQL_SCHEMA = """
        schema {
          query: Query
        }
        
        type ActionInfo {
          name: String!
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
        }
        
        scalar Duration
        
        type IntList {
          count: Int!
          records(limit: Int = 20, offset: Int = 0): [Int!]!
          __actions: [ActionInfo!]!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Query {
          get(input: [Int!]!): IntList!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "IntList",
            "pk_field": None,
            "actions": []
          }
        ],
        "__actions": [
          {
            "name": "get",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          }
        ]
      }
    }

    def test_request_no_pag(self):
        resp = self.query(
            """
            query{
              get(input: [1,2,3,4,5,6,7,8,9]){
                count
                records
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "records": [
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

    def test_request_pag(self):
        resp = self.query(
            """
            query{
              get(input: [1,2,3,4,5,6,7,8,9]){
                count
                records(limit: 3, offset: 2)
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "records": [
                        3,
                        4,
                        5
                    ]
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
