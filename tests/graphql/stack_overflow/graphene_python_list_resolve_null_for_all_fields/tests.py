from .objects import schema
from tests.graphql.graphql_test_utils import remove_ws, GraphQLTestCase


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
          users: [User!]!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TypeInfo {
          typename: String!
          fields: [FieldInfo!]!
          __str__: String!
        }
        
        type User {
          id: Int
          username: String
          email: String
          __str__: String!
          __actions: [ActionInfo!]!
        }
    """

    REF_META_SCHEMA = {
        "data": {
            "__types": [
                {
                    "typename": "User",
                    "fields": [
                        {
                            "name": "id",
                            "typename": "Integer"
                        },
                        {
                            "name": "username",
                            "typename": "String"
                        },
                        {
                            "name": "email",
                            "typename": "String"
                        }
                    ]
                }
            ],
            "__objects": [],
            "__actions": [
                {
                    "name": "users",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[User!]!",
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
              users{
                id
                username
                email
              }
            }
            """
        )

        exp = {
            "data": {
                "users": [
                    {
                        "id": 39330,
                        "username": "RCraig",
                        "email": "WRussell@dolor.gov"
                    },
                    {
                        "id": 39331,
                        "username": "AHohmann",
                        "email": "AMarina@sapien.com"
                    }
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
