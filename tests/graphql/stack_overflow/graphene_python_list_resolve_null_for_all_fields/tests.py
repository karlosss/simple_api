from .objects import schema
from tests.graphql.graphql_test_utils import remove_ws, GraphQLTestCase


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
                  users: [User!]!
                }

                type User {
                  id: Int
                  username: String
                  email: String
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              users{
                id
                username
                email
              }
            }
            """
        )

        exp = {
            "data": {
                "users": [
                    {
                        "id": 39330,
                        "username": "RCraig",
                        "email": "WRussell@dolor.gov"
                    },
                    {
                        "id": 39331,
                        "username": "AHohmann",
                        "email": "AMarina@sapien.com"
                    }
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
