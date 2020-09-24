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

                type IntList {
                  count: Int!
                  allRecords: [Int!]!
                  records(limit: Int = 20, offset: Int = 0): IntList!
                }

                type Query {
                  get(data: [Int!]!): IntList!
                }
                """
            )
        )

    def test_request_no_pag(self):
        resp = self.query(
            """
            query{
              get(data: [1,2,3,4,5,6,7,8,9]){
                count
                allRecords
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "allRecords": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9
                    ]
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_single_pag(self):
        resp = self.query(
            """
            query{
              get(data: [1,2,3,4,5,6,7,8,9]){
                count
                allRecords
                records(limit: 5, offset: 2){
                  count
                  allRecords
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "allRecords": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9
                    ],
                    "records": {
                        "count": 5,
                        "allRecords": [
                            3,
                            4,
                            5,
                            6,
                            7
                        ]
                    }
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_recursive_pag(self):
        resp = self.query(
            """
            query{
              get(data: [1,2,3,4,5,6,7,8,9]){
                count
                allRecords
                records(limit: 5, offset: 2){
                  count
                  allRecords
                  records(limit: 3, offset: 1){
                    count
                    allRecords
                  }
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "allRecords": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9
                    ],
                    "records": {
                        "count": 5,
                        "allRecords": [
                            3,
                            4,
                            5,
                            6,
                            7
                        ],
                        "records": {
                            "count": 3,
                            "allRecords": [
                                4,
                                5,
                                6
                            ]
                        }
                    }
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
