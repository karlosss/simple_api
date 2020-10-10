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
                
                scalar Duration
                
                type Query {
                  get(in: Duration!): Duration!
                  getObject(in: TestObjectInput!): TestObject!
                }
                
                type TestObject {
                  duration: Duration!
                }
                
                input TestObjectInput {
                  duration: Duration!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query q{
              get(in: "2 days, 0:00:20.3")
              getObject(in: {duration: "12:34:56"}){
                duration
              }
            }
            """
        )

        exp = {
          "data": {
            "get": "2 days, 0:00:20.300000",
            "getObject": {
              "duration": "12:34:56"
            }
          }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
