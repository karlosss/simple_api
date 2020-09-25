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
                  get(default: TestObjectInput!): TestObject!
                }

                type TestObject {
                  number(num: Int): Int!
                  number_def(num: Int = 5): Int!
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
                number_def
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "number": 50,
                    "number_def": 5
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
