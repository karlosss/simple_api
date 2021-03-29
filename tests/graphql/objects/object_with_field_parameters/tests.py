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
          get: TestObject!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          number(num: Int): Int!
          number_def(num: Int = 5): Int!
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
                            "name": "number",
                            "typename": "Integer!"
                        },
                        {
                            "name": "number_def",
                            "typename": "Integer!"
                        }
                    ]
                }
            ],
            "__objects": [],
            "__actions": [
                {
                    "name": "get",
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
    }

    def test_request_with_param(self):
        resp = self.query(
            """
            query{
              get{
                number(num: 30)
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "number": 30
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_no_param(self):
        resp = self.query(
            """
            query{
              get{
                number
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "number": 20
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_no_param_def(self):
        resp = self.query(
            """
            query{
              get{
                number_def
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "number_def": 5
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_no_param_def_with_value(self):
        resp = self.query(
            """
            query{
              get{
                number_def(num: 60)
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "number_def": 60
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
