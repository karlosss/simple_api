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
        
        type Person {
          name: String!
          age: Int!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input PersonInput {
          name: String!
          age: Int!
        }
        
        type PersonList {
          count: Int!
          records(limit: Int = 20, offset: Int = 0): [Person!]!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        type Query {
          get(input: [PersonInput!]!): PersonList!
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
            "__types": [
                {
                    "typename": "Person",
                    "fields": [
                        {
                            "name": "name",
                            "typename": "String!"
                        },
                        {
                            "name": "age",
                            "typename": "Integer!"
                        }
                    ]
                },
                {
                    "typename": "PersonList",
                    "fields": [
                        {
                            "name": "count",
                            "typename": "Integer!"
                        },
                        {
                            "name": "records",
                            "typename": "[Person!]!"
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
                            "name": "input",
                            "typename": "[Person!]!",
                            "default": None
                        }
                    ],
                    "data": [],
                    "mutation": False,
                    "return_type": "PersonList!",
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
              get(input: [
                {name: "Alice", age: 1},
                {name: "Bob", age: 2},
                {name: "Cindy", age: 3},
                {name: "Dan", age: 4},
              ]){
                count
                records{
                  name
                  age
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 4,
                    "records": [
                        {
                            "name": "Alice",
                            "age": 1
                        },
                        {
                            "name": "Bob",
                            "age": 2
                        },
                        {
                            "name": "Cindy",
                            "age": 3
                        },
                        {
                            "name": "Dan",
                            "age": 4
                        }
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
              get(input: [
                {name: "Alice", age: 1},
                {name: "Bob", age: 2},
                {name: "Cindy", age: 3},
                {name: "Dan", age: 4},
              ]){
                count
                records(limit: 1, offset: 1){
                  name
                  age
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 4,
                    "records": [
                        {
                            "name": "Bob",
                            "age": 2
                        }
                    ]
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
