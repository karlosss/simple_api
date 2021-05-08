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
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
          __str__: String!
        }
        
        type Query {
          getNonNull: [Int!]!
          getNull: [Int]
          getListNullElemNonNull: [Int!]
          getListNonNullElemNull: [Int]!
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
            "__types": [],
            "__objects": [],
            "__actions": [
                {
                    "name": "getNonNull",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[Integer!]!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getNull",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[Integer]",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getListNullElemNonNull",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[Integer!]",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getListNonNullElemNull",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[Integer]!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                }
            ]
        }
    }

    def test_request_non_null(self):
        resp = self.query(
            """
            query{
              getNonNull
            }
            """
        )

        exp = {
            "data": {
                "getNonNull": [
                    0,
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

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_null_elem_non_null(self):
        resp = self.query(
            """
            query{
              getListNullElemNonNull
            }
            """
        )

        exp = {
            "data": {
                "getListNullElemNonNull": None
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_non_null_elem_null(self):
        resp = self.query(
            """
            query{
              getListNonNullElemNull
            }
            """
        )

        exp = {
            "data": {
                "getListNonNullElemNull": [
                    1,
                    2,
                    3,
                    None,
                    None,
                    None,
                    7,
                    8,
                    9
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
