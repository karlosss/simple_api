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
                
                type NonNullableObject {
                  allowed_field: String!
                  forbidden_field: String!
                }
                
                type NullableObject {
                  allowed_field: String
                  forbidden_field: String
                }
                
                type Query {
                  NonNullableObjectAllowedGet: NonNullableObject!
                  NonNullableObjectForbiddenGet: NonNullableObject!
                  NullableObjectAllowedGet: NullableObject
                  NullableObjectForbiddenGet: NullableObject
                }
                """
            )
        )

    def test_non_nullable_permission_fail(self):
        resp = self.query(
            """
            query{
              NonNullableObjectAllowedGet{
                allowed_field
                forbidden_field
              }
            }
            """
        )

        exp = {
          "errors": [
            {
              "message": "You do not have permission to access this.",
              "locations": [
                {
                  "line": 5,
                  "column": 17
                }
              ],
              "path": [
                "NonNullableObjectAllowedGet",
                "forbidden_field"
              ]
            }
          ],
          "data": None
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_nullable_permission_fail(self):
        resp = self.query(
            """
            query{
              NullableObjectAllowedGet{
                allowed_field
                forbidden_field
              }
            }
            """
        )

        exp = {
          "errors": [
            {
              "message": "You do not have permission to access this.",
              "locations": [
                {
                  "line": 5,
                  "column": 17
                }
              ],
              "path": [
                "NullableObjectAllowedGet",
                "forbidden_field"
              ]
            }
          ],
          "data": {
            "NullableObjectAllowedGet": {
              "allowed_field": "allowed",
              "forbidden_field": None
            }
          }
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)
