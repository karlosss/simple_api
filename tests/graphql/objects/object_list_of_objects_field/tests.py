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
                  getNonNull: [TestObject!]!
                  getNull: [TestObject]
                  getListNullElemNonNull: [TestObject!]
                  getListNonNullElemNull: [TestObject]!
                }

                type TestObject {
                  int1: Int!
                  int2: Int!
                }
                """
            )
        )

    def test_request_non_null(self):
        resp = self.query(
            """
            query{
              getNonNull{
                int1
                int2
              }
            }
            """
        )

        exp = {
            "data": {
                "getNonNull": [
                    {
                        "int1": 0,
                        "int2": 10
                    },
                    {
                        "int1": 1,
                        "int2": 11
                    },
                    {
                        "int1": 2,
                        "int2": 12
                    }
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_null_elem_non_null(self):
        resp = self.query(
            """
            query{
              getListNullElemNonNull{
                int1
                int2
              }
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
              getListNonNullElemNull{
                int1
                int2
              }
            }
            """
        )

        exp = {
            "data": {
                "getListNonNullElemNull": [
                    {
                        "int1": 0,
                        "int2": 10
                    },
                    None,
                    {
                        "int1": 2,
                        "int2": 12
                    }
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
