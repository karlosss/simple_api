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

                scalar Date

                scalar DateTime

                type Query {
                  getObject: TestObject!
                  getDate: Date!
                  getTime: Time!
                  getDatetime: DateTime!
                  echo(date: Date!, time: Time!, datetime: DateTime!): TestObject!
                }

                type TestObject {
                  date: Date!
                  time: Time!
                  datetime: DateTime!
                }

                scalar Time
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query {
              getObject{
                date
                time
                datetime
              }
              getDate
              getTime
              getDatetime
              echo(date: "2020-01-01", time: "12:34:56", datetime: "2020-01-01T12:34:56"){
                date
                time
                datetime
              }
            }
            """
        )

        exp = {
            "data": {
                "getObject": {
                    "date": "2020-01-01",
                    "time": "12:34:56",
                    "datetime": "2020-01-01T12:34:56"
                },
                "getDate": "2020-01-01",
                "getTime": "12:34:56",
                "getDatetime": "2020-01-01T12:34:56",
                "echo": {
                    "date": "2020-01-01",
                    "time": "12:34:56",
                    "datetime": "2020-01-01T12:34:56"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
