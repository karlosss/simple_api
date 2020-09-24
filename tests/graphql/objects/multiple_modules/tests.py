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

                type A {
                  s1: String!
                  s2: A
                }

                type B {
                  s1: String!
                  s2: B
                }

                type C {
                  a: A!
                  b: B!
                }

                type Query {
                  get: C!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              get{
                a{
                  s1
                  s2{
                    s2{
                      s1
                    }
                  }
                }
                b{
                  s1
                  s2{
                    s2{
                      s1
                    }
                  }
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "a": {
                        "s1": "A",
                        "s2": None
                    },
                    "b": {
                        "s1": "B",
                        "s2": None
                    }
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
