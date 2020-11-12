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
          get(in: Duration!): Duration!
          getObject(in: TestObjectInput!): TestObject!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          duration: Duration!
          __actions: [ActionInfo!]!
        }
        
        input TestObjectInput {
          duration: Duration!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "TestObject",
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
          },
          {
            "name": "getObject",
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
            query q{
              get(in: "2 days, 0:00:20.3")
              getObject(in: {duration: "12:34:56"}){
                duration
              }
            }
            """
        )

        exp = {
          "data": {
            "get": "2 days, 0:00:20.300000",
            "getObject": {
              "duration": "12:34:56"
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
