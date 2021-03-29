from .objects import schema
from tests.graphql.graphql_test_utils import GraphQLTestCase, remove_ws


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    REF_GRAPHQL_SCHEMA = """
        schema {
          query: Query
        }
        
        type ActionInfo {
          name: String!
          parameters: [FieldInfo!]!
          data: [FieldInfo!]!
          return_type: String!
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
          mutation: Boolean!
          __str__: String!
        }
        
        scalar Duration
        
        type FieldInfo {
          name: String!
          typename: String!
          default: String
          __str__: String!
        }
        
        type IntList {
          count: Int!
          all_records: [Int!]!
          records(limit: Int = 20, offset: Int = 0): IntList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
          __str__: String!
        }
        
        type Query {
          get(input: [Int!]!): IntList!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TypeInfo {
          typename: String!
          fields: [FieldInfo!]!
          __str__: String!
        }
    """

    REF_META_SCHEMA = {
        "data": {
            "__types": [
                {
                    "typename": "IntList",
                    "fields": [
                        {
                            "name": "count",
                            "typename": "Integer!"
                        },
                        {
                            "name": "all_records",
                            "typename": "[Integer!]!"
                        },
                        {
                            "name": "records",
                            "typename": "IntList!"
                        }
                    ]
                }
            ],
            "__objects": [],
            "__actions": [
                {
                    "name": "get",
                    "parameters": [
                        {
                            "name": "input",
                            "typename": "[Integer!]!",
                            "default": None
                        }
                    ],
                    "data": [],
                    "mutation": False,
                    "return_type": "IntList!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                }
            ]
        }
    }

    def test_request_no_pag(self):
        resp = self.query(
            """
            query{
              get(input: [1,2,3,4,5,6,7,8,9]){
                count
                all_records
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "all_records": [
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
              get(input: [1,2,3,4,5,6,7,8,9]){
                count
                all_records
                records(limit: 5, offset: 2){
                  count
                  all_records
                }
              }
            }
            """
        )

        exp = {
            "data": {
                "get": {
                    "count": 9,
                    "all_records": [
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
                        "all_records": [
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
              get(input: [1,2,3,4,5,6,7,8,9]){
                count
                all_records
                records(limit: 5, offset: 2){
                  count
                  all_records
                  records(limit: 3, offset: 1){
                    count
                    all_records
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
                    "all_records": [
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
                        "all_records": [
                            3,
                            4,
                            5,
                            6,
                            7
                        ],
                        "records": {
                            "count": 3,
                            "all_records": [
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
