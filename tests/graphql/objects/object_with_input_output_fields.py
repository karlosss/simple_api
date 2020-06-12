from graphene_django.utils import GraphQLTestCase

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, PlainListType, ObjectType, StringType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


class TestObject(Object):
    fields = {
        "field": IntegerType(),
        "nullable_if_input_field": IntegerType(nullable_if_input=True),
    }
    input_fields = {
        "only_input_field": IntegerType()
    }
    output_fields = {
        "only_output_field": IntegerType(nullable=True)
    }


def get(request, params):
    return {
        "field": 1,
        "nullable_if_input_field": 2
    }


actions = {
    "get": Action({"in": ObjectType(TestObject)}, ObjectType(TestObject), Function(get))
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
                  get(in: TestObjectInput!): TestObject!
                }
                
                type TestObject {
                  field: Int!
                  nullableIfInputField: Int!
                  onlyOutputField: Int
                }
                
                input TestObjectInput {
                  field: Int!
                  nullableIfInputField: Int
                  onlyInputField: Int!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              get(in: {field: 4, onlyInputField: 6}){
                field
                nullableIfInputField
                onlyOutputField
              }
            }
            """
        )

        exp = {
          "data": {
            "get": {
              "field": 1,
              "nullableIfInputField": 2,
              "onlyOutputField": None
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
