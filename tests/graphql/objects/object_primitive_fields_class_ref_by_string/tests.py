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
          TestObjectNonNullOnly: TestObject!
          TestObjectNonNullAndNull: TestObject!
          TestObjectAll: TestObject!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          string_non_null: String!
          string_null: String
          string_default: String!
          __str__: String!
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
            "__types": [
                {
                    "typename": "TestObject",
                    "fields": [
                        {
                            "name": "string_non_null",
                            "typename": "String!"
                        },
                        {
                            "name": "string_null",
                            "typename": "String"
                        },
                        {
                            "name": "string_default",
                            "typename": "String!"
                        }
                    ]
                }
            ],
            "__objects": [
                {
                    "name": "TestObject",
                    "pk_field": None,
                    "actions": [
                        {
                            "name": "TestObjectNonNullOnly",
                            "parameters": [],
                            "data": [],
                            "mutation": False,
                            "return_type": "TestObject!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "TestObjectNonNullAndNull",
                            "parameters": [],
                            "data": [],
                            "mutation": False,
                            "return_type": "TestObject!",
                            "permitted": True,
                            "deny_reason": None,
                            "retry_in": None
                        },
                        {
                            "name": "TestObjectAll",
                            "parameters": [],
                            "data": [],
                            "mutation": False,
                            "return_type": "TestObject!",
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
