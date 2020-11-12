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
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
        }
        
        scalar Duration
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Query {
          getNonNull: [Int!]!
          getNull: [Int]
          getListNullElemNonNull: [Int!]
          getListNonNullElemNull: [Int]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [],
        "__actions": [
          {
            "name": "getNonNull",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          },
          {
            "name": "getNull",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          },
          {
            "name": "getListNullElemNonNull",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          },
          {
            "name": "getListNonNullElemNull",
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
