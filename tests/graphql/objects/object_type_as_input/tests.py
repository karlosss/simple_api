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
                  get(id: TestObjectInput!): String!
                  getNull(id: TestObjectInput): String!
                  getNullDefault(id: TestObjectInput = {int1: 10, int2: 20}): String!
                }

                input TestObjectInput {
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
              get(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
            "data": {
                "get": "1.2"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_non_null_fail(self):
        resp = self.query(
            """
            query{
              get
            }
            """
        )

        self.assertResponseHasErrors(resp)

    def test_request_null_param(self):
        resp = self.query(
            """
            query{
              getNull(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
            "data": {
                "getNull": "1.2"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_no_param(self):
        resp = self.query(
            """
            query{
              getNull
            }
            """
        )

        exp = {
            "data": {
                "getNull": "no params passed"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_default_no_param(self):
        resp = self.query(
            """
            query{
              getNullDefault
            }
            """
        )

        exp = {
            "data": {
                "getNullDefault": "10.20"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_default_with_param(self):
        resp = self.query(
            """
            query{
              getNullDefault(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
            "data": {
                "getNullDefault": "1.2"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)