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
                  TestObjectNonNullOnly: TestObject!
                  TestObjectNonNullAndNull: TestObject!
                  TestObjectAll: TestObject!
                }

                type TestObject {
                  string_non_null: String!
                  string_null: String
                  string_default: String!
                }
                """
            )
        )

    def test_request_non_null_only(self):
        resp = self.query(
            """
            query{
              TestObjectNonNullOnly{
                string_non_null
                string_null
                string_default
              }
            }
            """
        )

        exp = {
            "data": {
                "TestObjectNonNullOnly": {
                    "string_non_null": "string",
                    "string_null": None,
                    "string_default": "default"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_non_null_and_null(self):
        resp = self.query(
            """
            query{
              TestObjectNonNullAndNull{
                string_non_null
                string_null
                string_default
              }
            }
            """
        )

        exp = {
            "data": {
                "TestObjectNonNullAndNull": {
                    "string_non_null": "string",
                    "string_null": "string",
                    "string_default": "default"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_all(self):
        resp = self.query(
            """
            query{
              TestObjectAll{
                string_non_null
                string_null
                string_default
              }
            }
            """
        )

        exp = {
            "data": {
                "TestObjectAll": {
                    "string_non_null": "string",
                    "string_null": "string",
                    "string_default": "string"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
