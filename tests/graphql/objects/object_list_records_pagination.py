from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, PlainListType, ObjectType, StringType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def resolve(request, parent_val, params):
    return parent_val["records"][params["offset"]:(params["offset"] + params["limit"])]


class Person(Object):
    fields = {
        "name": StringType(),
        "age": IntegerType(),
    }


class PersonList(Object):
    fields = {
        "count": IntegerType(),
        "records": PlainListType(
            ObjectType(Person),
            parameters={
                "limit": IntegerType(nullable=True, default=20),
                "offset": IntegerType(nullable=True, default=0),
            },
            resolver=Function(resolve)
        )
    }


def get(request, params):
    return {
        "count": len(params["data"]),
        "records": params["data"]
    }


class Actions(Object):
    actions = {
        "get": Action({"data": PlainListType(ObjectType(Person))}, ObjectType(PersonList), Function(get))
    }


schema = generate(GraphQLAdapter, [Actions, PersonList, Person])


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
                
                type Person {
                  name: String!
                  age: Int!
                }
                
                input PersonInput {
                  name: String!
                  age: Int!
                }
                
                type PersonList {
                  count: Int!
                  records(limit: Int = 20, offset: Int = 0): [Person!]!
                }
                
                type Query {
                  get(data: [PersonInput!]!): PersonList!
                }
                """
            )
        )

    def test_request_no_pag(self):
        resp = self.query(
            """
            query{
              get(data: [
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
              get(data: [
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
