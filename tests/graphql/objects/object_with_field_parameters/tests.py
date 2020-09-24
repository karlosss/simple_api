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
                  get: TestObject!
                }

                type TestObject {
                  number(num: Int): Int!
                  numberDef(num: Int = 5): Int!
                }
                """
            )
        )

    def test_request_with_param(self):
        resp = self.query(
            """
            query{
              get{
                number(num: 30)
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "number": 30
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_no_param(self):
        resp = self.query(
            """
            query{
              get{
                number
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "number": 20
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_no_param_def(self):
        resp = self.query(
            """
            query{
              get{
                numberDef
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "numberDef": 5
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_no_param_def_with_value(self):
        resp = self.query(
            """
            query{
              get{
                numberDef(num: 60)
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "numberDef": 60
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
