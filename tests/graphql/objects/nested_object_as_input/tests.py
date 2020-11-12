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
        
        type Coordinates {
          lat: Int!
          lng: Int!
          __actions: [ActionInfo!]!
        }
        
        input CoordinatesInput {
          lat: Int!
          lng: Int!
        }
        
        scalar Duration
        
        type Location {
          name: String!
          coords: Coordinates!
          __actions: [ActionInfo!]!
        }
        
        input LocationInput {
          name: String!
          coords: CoordinatesInput!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Query {
          echo(loc: LocationInput!): Location!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "Coordinates",
            "pk_field": None,
            "actions": []
          },
          {
            "name": "Location",
            "pk_field": None,
            "actions": []
          }
        ],
        "__actions": [
          {
            "name": "echo",
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
              echo(loc: {name: "Place", coords: {lat: 10, lng: 20}}){
                name
                coords{
                  lat
                  lng
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "echo": {
                    "name": "Place",
                    "coords": {
                        "lat": 10,
                        "lng": 20
                    }
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
