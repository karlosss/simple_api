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
          TestObjectNonNullOnly: TestObject!
          TestObjectNonNullAndNull: TestObject!
          TestObjectAll: TestObject!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          string_non_null: String!
          string_null: String
          string_default: String!
          __actions: [ActionInfo!]!
        }

    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "TestObject",
            "pk_field": None,
            "actions": [
              {
                "name": "TestObjectNonNullOnly",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              },
              {
                "name": "TestObjectNonNullAndNull",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              },
              {
                "name": "TestObjectAll",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              }
            ]
          }
        ],
        "__actions": []
      }
    }

    def test_request_non_null_only(self):
        resp = self.query(
            """
            query{
              TestObjectNonNullOnly{
                string_non_null
                string_null
                string_default
              }
            }
            """
        )

        exp = {
            "data": {
                "TestObjectNonNullOnly": {
                    "string_non_null": "string",
                    "string_null": None,
                    "string_default": "default"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_non_null_and_null(self):
        resp = self.query(
            """
            query{
              TestObjectNonNullAndNull{
                string_non_null
                string_null
                string_default
              }
            }
            """
        )

        exp = {
            "data": {
                "TestObjectNonNullAndNull": {
                    "string_non_null": "string",
                    "string_null": "string",
                    "string_default": "default"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_all(self):
        resp = self.query(
            """
            query{
              TestObjectAll{
                string_non_null
                string_null
                string_default
              }
            }
            """
        )

        exp = {
            "data": {
                "TestObjectAll": {
                    "string_non_null": "string",
                    "string_null": "string",
                    "string_default": "string"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
