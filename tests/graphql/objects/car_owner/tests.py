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
        
        type Car {
          model: String!
          color: String!
          __actions: [ActionInfo!]!
        }
        
        scalar Duration
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Owner {
          id: Int!
          car: Car!
          __actions: [ActionInfo!]!
        }
        
        type Query {
          OwnerGetById(id: Int!): Owner!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "Car",
            "pk_field": None,
            "actions": []
          },
          {
            "name": "Owner",
            "pk_field": None,
            "actions": [
              {
                "name": "OwnerGetById",
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

    def test_request(self):
        resp = self.query(
            """
            query{
              OwnerGetById(id: 42){
                id
                car{
                  model
                  color
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "OwnerGetById": {
                    "id": 42,
                    "car": {
                        "model": "BMW",
                        "color": "blue"
                    }
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
