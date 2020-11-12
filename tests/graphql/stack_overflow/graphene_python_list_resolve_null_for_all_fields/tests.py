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
          users: [User!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type User {
          id: Int
          username: String
          email: String
          __actions: [ActionInfo!]!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "User",
            "pk_field": None,
            "actions": []
          }
        ],
        "__actions": [
          {
            "name": "users",
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
