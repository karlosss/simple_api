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
          __actions: [ActionInfo!]!
        }
        
        type ActionInfo {
          name: String!
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
        }
        
        type B {
          s1: String!
          s2: B
          __actions: [ActionInfo!]!
        }
        
        type C {
          a: A!
          b: B!
          __actions: [ActionInfo!]!
        }
        
        scalar Duration
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Query {
          get: C!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "A",
            "pk_field": None,
            "actions": []
          },
          {
            "name": "B",
            "pk_field": None,
            "actions": []
          },
          {
            "name": "C",
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
