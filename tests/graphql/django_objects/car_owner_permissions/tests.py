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
                
                type Car {
                  model: String!
                  color: String!
                }
                
                type Owner {
                  id: Int!
                  car: Car!
                }
                
                type Query {
                  OwnerGetById(id: Int!): Owner!
                }
                """
            )
        )

    def test_request(self):
        resp = self.query(
            """
            query{
              OwnerGetById(id: 42){
                id
                car{
                  model
                  color
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "OwnerGetById": {
                    "id": 42,
                    "car": {
                        "model": "BMW",
                        "color": "blue"
                    }
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
