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

                type Person {
                  name: String!
                  age: Int!
                }

                input PersonInput {
                  name: String!
                  age: Int!
                }

                type PersonList {
                  count: Int!
                  records(limit: Int = 20, offset: Int = 0): [Person!]!
                }

                type Query {
                  get(data: [PersonInput!]!): PersonList!
                }
                """
            )
        )

    def test_request_no_pag(self):
        resp = self.query(
            """
            query{
              get(data: [
                {name: "Alice", age: 1},
                {name: "Bob", age: 2},
                {name: "Cindy", age: 3},
                {name: "Dan", age: 4},
              ]){
                count
                records{
                  name
                  age
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 4,
                    "records": [
                        {
                            "name": "Alice",
                            "age": 1
                        },
                        {
                            "name": "Bob",
                            "age": 2
                        },
                        {
                            "name": "Cindy",
                            "age": 3
                        },
                        {
                            "name": "Dan",
                            "age": 4
                        }
                    ]
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_pag(self):
        resp = self.query(
            """
            query{
              get(data: [
                {name: "Alice", age: 1},
                {name: "Bob", age: 2},
                {name: "Cindy", age: 3},
                {name: "Dan", age: 4},
              ]){
                count
                records(limit: 1, offset: 1){
                  name
                  age
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 4,
                    "records": [
                        {
                            "name": "Bob",
                            "age": 2
                        }
                    ]
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
