from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import ObjectType, IntegerType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def get(request, params):
    return params["default"]["number"]


class TestObject(Object):
    def get_number(request, parent_val, params):
        return params.get("num") or parent_val

    fields = {
        "number": IntegerType(parameters={"num": IntegerType(nullable=True)}, resolver=Function(get_number)),
    }

    output_fields = {
        "number_def": IntegerType(parameters={"num": IntegerType(nullable=True, default=5)},
                                  resolver=Function(get_number)),
    }


actions = {
    "get": Action(parameters={"default": ObjectType(TestObject)}, return_value=ObjectType(TestObject), exec_fn=Function(get))
}

schema = generate(GraphQLAdapter, [TestObject], actions)


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
                
                type Query {
                  get(default: TestObjectInput!): TestObject!
                }
                
                type TestObject {
                  number(num: Int): Int!
                  numberDef(num: Int = 5): Int!
                }
                
                input TestObjectInput {
                  number: Int!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              get(default: {number: 50}){
                number
                numberDef
              }
            }
            """
        )

        exp = {
          "data": {
            "get": {
              "number": 50,
              "numberDef": 5
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
