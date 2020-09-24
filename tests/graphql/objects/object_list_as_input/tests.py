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
                  plusOne(list: [Int!]!): [Int!]!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              plusOne(list: [1, 2, 3, 4])
            }
            """
        )

        exp = {
            "data": {
                "plusOne": [
                    2,
                    3,
                    4,
                    5
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
