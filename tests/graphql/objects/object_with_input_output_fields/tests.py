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
          get(in: TestObjectInput!): TestObject!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          field: Int!
          nullable_if_input_field: Int!
          only_output_field: Int
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input TestObjectInput {
          field: Int!
          nullable_if_input_field: Int
          only_input_field: Int!
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
                            "name": "field",
                            "typename": "Integer!"
                        },
                        {
                            "name": "nullable_if_input_field",
                            "typename": "Integer!"
                        },
                        {
                            "name": "only_output_field",
                            "typename": "Integer"
                        }
                    ]
                }
            ],
            "__objects": [],
            "__actions": [
                {
                    "name": "get",
                    "parameters": [
                        {
                            "name": "in",
                            "typename": "TestObject!",
                            "default": None
                        }
                    ],
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

    def test_request(self):
        resp = self.query(
            """
            query{
              get(in: {field: 4, only_input_field: 6}){
                field
                nullable_if_input_field
                only_output_field
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "field": 1,
                    "nullable_if_input_field": 2,
                    "only_output_field": None
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
