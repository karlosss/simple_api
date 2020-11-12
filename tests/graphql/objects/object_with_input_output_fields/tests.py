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
          get(in: TestObjectInput!): TestObject!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          field: Int!
          nullable_if_input_field: Int!
          only_output_field: Int
          __actions: [ActionInfo!]!
        }
        
        input TestObjectInput {
          field: Int!
          nullable_if_input_field: Int
          only_input_field: Int!
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
