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
