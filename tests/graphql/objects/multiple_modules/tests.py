from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase, remove_ws


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    REF_GRAPHQL_SCHEMA = """
        schema {
          query: Query
        }
        
        type A {
          s1: String!
          s2: A
          __str__: String!
          __actions: [ActionInfo!]!
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
        
        type B {
          s1: String!
          s2: B
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        type C {
          a: A!
          b: B!
          __str__: String!
          __actions: [ActionInfo!]!
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
          get: C!
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
                    "typename": "A",
                    "fields": [
                        {
                            "name": "s1",
                            "typename": "String!"
                        },
                        {
                            "name": "s2",
                            "typename": "A"
                        }
                    ]
                },
                {
                    "typename": "B",
                    "fields": [
                        {
                            "name": "s1",
                            "typename": "String!"
                        },
                        {
                            "name": "s2",
                            "typename": "B"
                        }
                    ]
                },
                {
                    "typename": "C",
                    "fields": [
                        {
                            "name": "a",
                            "typename": "A!"
                        },
                        {
                            "name": "b",
                            "typename": "B!"
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
                    "return_type": "C!",
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
              get{
                a{
                  s1
                  s2{
                    s2{
                      s1
                    }
                  }
                }
                b{
                  s1
                  s2{
                    s2{
                      s1
                    }
                  }
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "a": {
                        "s1": "A",
                        "s2": None
                    },
                    "b": {
                        "s1": "B",
                        "s2": None
                    }
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
