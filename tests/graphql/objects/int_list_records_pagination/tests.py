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

                type IntList {
                  count: Int!
                  records(limit: Int = 20, offset: Int = 0): [Int!]!
                }

                type Query {
                  get(data: [Int!]!): IntList!
                }
                """
            )
        )

    def test_request_no_pag(self):
        resp = self.query(
            """
            query{
              get(data: [1,2,3,4,5,6,7,8,9]){
                count
                records
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "records": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9
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
              get(data: [1,2,3,4,5,6,7,8,9]){
                count
                records(limit: 3, offset: 2)
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "records": [
                        3,
                        4,
                        5
                    ]
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
