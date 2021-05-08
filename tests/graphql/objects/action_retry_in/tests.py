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
          parameters: [FieldInfo!]!
          data: [FieldInfo!]!
          return_type: String!
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
          mutation: Boolean!
          __str__: String!
        }
        
        scalar Duration
        
        type FieldInfo {
          name: String!
          typename: String!
          default: String
          __str__: String!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
          __str__: String!
        }
        
        type Query {
          allow: Boolean!
          deny: Boolean!
          hide: Boolean!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TypeInfo {
          typename: String!
          fields: [FieldInfo!]!
          __str__: String!
        }
        """
    REF_META_SCHEMA = {
      "data": {
        "__types": [],
        "__objects": [],
        "__actions": [
          {
            "name": "allow",
            "parameters": [],
            "data": [],
            "mutation": False,
            "return_type": "Boolean!",
            "permitted": True,
            "deny_reason": None,
            "retry_in": "1:00:00"
          },
          {
            "name": "deny",
            "parameters": [],
            "data": [],
            "mutation": False,
            "return_type": "Boolean!",
            "permitted": False,
            "deny_reason": "You do not have permission to access this.",
            "retry_in": "3 days, 0:00:10"
          }
        ]
      }
    }

    def test_allow(self):
        resp = self.query(
            """
            query{
              allow
            }
            """
        )

        exp = {
          "data": {
            "allow": True
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_deny(self):
        resp = self.query(
            """
            query{
              deny
            }
            """
        )

        exp = {
          "errors": [
            {
              "message": "You do not have permission to access this.",
              "locations": [
                {
                  "line": 3,
                  "column": 15
                }
              ],
              "path": [
                "deny"
              ]
            }
          ],
          "data": None
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_hide(self):
        resp = self.query(
            """
            query{
              hide
            }
            """
        )

        exp = {
          "errors": [
            {
              "message": "You do not have permission to access this.",
              "locations": [
                {
                  "line": 3,
                  "column": 15
                }
              ],
              "path": [
                "hide"
              ]
            }
          ],
          "data": None
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)
