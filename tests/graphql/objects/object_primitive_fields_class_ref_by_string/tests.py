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
                  testObjectNonNullOnly: TestObject!
                  testObjectNonNullAndNull: TestObject!
                  testObjectAll: TestObject!
                }

                type TestObject {
                  stringNonNull: String!
                  stringNull: String
                  stringDefault: String!
                }
                """
            )
        )

    def test_request_non_null_only(self):
        resp = self.query(
            """
            query{
              testObjectNonNullOnly{
                stringNonNull
                stringNull
                stringDefault
              }
            }
            """
        )

        exp = {
            "data": {
                "testObjectNonNullOnly": {
                    "stringNonNull": "string",
                    "stringNull": None,
                    "stringDefault": "default"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_non_null_and_null(self):
        resp = self.query(
            """
            query{
              testObjectNonNullAndNull{
                stringNonNull
                stringNull
                stringDefault
              }
            }
            """
        )

        exp = {
            "data": {
                "testObjectNonNullAndNull": {
                    "stringNonNull": "string",
                    "stringNull": "string",
                    "stringDefault": "default"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_all(self):
        resp = self.query(
            """
            query{
              testObjectAll{
                stringNonNull
                stringNull
                stringDefault
              }
            }
            """
        )

        exp = {
            "data": {
                "testObjectAll": {
                    "stringNonNull": "string",
                    "stringNull": "string",
                    "stringDefault": "string"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
