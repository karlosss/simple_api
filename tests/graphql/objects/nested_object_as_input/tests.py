from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase, remove_ws


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_schema(self):
        self.assertEqual(
            remove_ws(str(self.GRAPHQL_SCHEMA)),
            remove_ws(
                """
                schema {
                  query: Query
                }

                type Coordinates {
                  lat: Int!
                  lng: Int!
                }

                input CoordinatesInput {
                  lat: Int!
                  lng: Int!
                }

                type Location {
                  name: String!
                  coords: Coordinates!
                }

                input LocationInput {
                  name: String!
                  coords: CoordinatesInput!
                }

                type Query {
                  echo(loc: LocationInput!): Location!
                }
                """
            )
        )

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
