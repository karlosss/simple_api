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
          allow: Boolean!
          deny: Boolean!
          hide: Boolean!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        """
    REF_META_SCHEMA = {
        "data": {
            "__objects": [],
            "__actions": [
              {
                "name": "allow",
                "permitted": True,
                "deny_reason": None,
                "retry_in": "1:00:00"
              },
              {
                "name": "deny",
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
