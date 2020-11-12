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
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Query {
          plusOne(list: [Int!]!): [Int!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }

    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [],
        "__actions": [
          {
            "name": "plusOne",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          }
        ]
      }
    }

    def test_request(self):
        resp = self.query(
            """
            query{
              plusOne(list: [1, 2, 3, 4])
            }
            """
        )

        exp = {
            "data": {
                "plusOne": [
                    2,
                    3,
                    4,
                    5
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
