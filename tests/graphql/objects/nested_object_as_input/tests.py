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
        
        type Coordinates {
          lat: Int!
          lng: Int!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input CoordinatesInput {
          lat: Int!
          lng: Int!
        }
        
        scalar Duration
        
        type FieldInfo {
          name: String!
          typename: String!
          default: String
          __str__: String!
        }
        
        type Location {
          name: String!
          coords: Coordinates!
          __str__: String!
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
          __str__: String!
        }
        
        type Query {
          echo(loc: LocationInput!): Location!
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
                    "typename": "Coordinates",
                    "fields": [
                        {
                            "name": "lat",
                            "typename": "Integer!"
                        },
                        {
                            "name": "lng",
                            "typename": "Integer!"
                        }
                    ]
                },
                {
                    "typename": "Location",
                    "fields": [
                        {
                            "name": "name",
                            "typename": "String!"
                        },
                        {
                            "name": "coords",
                            "typename": "Coordinates!"
                        }
                    ]
                }
            ],
            "__objects": [],
            "__actions": [
                {
                    "name": "echo",
                    "parameters": [
                        {
                            "name": "loc",
                            "typename": "Location!",
                            "default": None
                        }
                    ],
                    "data": [],
                    "mutation": False,
                    "return_type": "Location!",
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
