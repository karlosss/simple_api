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
                  getNonNull: [Int!]!
                  getNull: [Int]
                  getListNullElemNonNull: [Int!]
                  getListNonNullElemNull: [Int]!
                }
                """
            )
        )

    def test_request_non_null(self):
        resp = self.query(
            """
            query{
              getNonNull
            }
            """
        )

        exp = {
            "data": {
                "getNonNull": [
                    0,
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

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_null_elem_non_null(self):
        resp = self.query(
            """
            query{
              getListNullElemNonNull
            }
            """
        )

        exp = {
            "data": {
                "getListNullElemNonNull": None
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_non_null_elem_null(self):
        resp = self.query(
            """
            query{
              getListNonNullElemNull
            }
            """
        )

        exp = {
            "data": {
                "getListNonNullElemNull": [
                    1,
                    2,
                    3,
                    None,
                    None,
                    None,
                    7,
                    8,
                    9
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
