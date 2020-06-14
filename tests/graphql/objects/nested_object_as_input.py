from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, PlainListType, ObjectType, StringType, BooleanType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


class Coordinates(Object):
    fields = {
        "lat": IntegerType(),
        "lng": IntegerType()
    }


class Location(Object):
    fields = {
        "name": StringType(),
        "coords": ObjectType(Coordinates)
    }


def echo(request, params):
    return params["loc"]


actions = {
    "echo": Action({"loc": ObjectType(Location)}, ObjectType(Location), Function(echo))
}

schema = generate(GraphQLAdapter, [Location, Coordinates], actions)


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = get_graphql_url(__file__)

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
