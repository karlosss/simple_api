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
                  nullable_if_input_field: Int!
                  only_output_field: Int
                }

                input TestObjectInput {
                  field: Int!
                  nullable_if_input_field: Int
                  only_input_field: Int!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              get(in: {field: 4, only_input_field: 6}){
                field
                nullable_if_input_field
                only_output_field
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "field": 1,
                    "nullable_if_input_field": 2,
                    "only_output_field": None
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
