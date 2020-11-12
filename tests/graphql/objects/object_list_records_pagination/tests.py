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
        
        type Person {
          name: String!
          age: Int!
          __actions: [ActionInfo!]!
        }
        
        input PersonInput {
          name: String!
          age: Int!
        }
        
        type PersonList {
          count: Int!
          records(limit: Int = 20, offset: Int = 0): [Person!]!
          __actions: [ActionInfo!]!
        }
        
        type Query {
          get(input: [PersonInput!]!): PersonList!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }

    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "Person",
            "pk_field": None,
            "actions": []
          },
          {
            "name": "PersonList",
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
