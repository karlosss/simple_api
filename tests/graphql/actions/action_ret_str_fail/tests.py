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
                  non_null: String!
                  null: String
                }
                """
            )
        )

    def test_request_non_null(self):
        resp = self.query(
            """
            query{
              non_null
            }
            """
        )

        self.assertResponseHasErrors(resp)

    def test_request_null(self):
        resp = self.query(
            """
            query{
              null
            }
            """
        )

        exp = {
          "data": {
            "null": "nonNull"
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
