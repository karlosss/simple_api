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
          getNonNull: [TestObject!]!
          getNull: [TestObject]
          getListNullElemNonNull: [TestObject!]
          getListNonNullElemNull: [TestObject]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          int1: Int!
          int2: Int!
          __actions: [ActionInfo!]!
        }

    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "TestObject",
            "pk_field": None,
            "actions": []
          }
        ],
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
              getNonNull{
                int1
                int2
              }
            }
            """
        )

        exp = {
            "data": {
                "getNonNull": [
                    {
                        "int1": 0,
                        "int2": 10
                    },
                    {
                        "int1": 1,
                        "int2": 11
                    },
                    {
                        "int1": 2,
                        "int2": 12
                    }
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_list_null_elem_non_null(self):
        resp = self.query(
            """
            query{
              getListNullElemNonNull{
                int1
                int2
              }
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
              getListNonNullElemNull{
                int1
                int2
              }
            }
            """
        )

        exp = {
            "data": {
                "getListNonNullElemNull": [
                    {
                        "int1": 0,
                        "int2": 10
                    },
                    None,
                    {
                        "int1": 2,
                        "int2": 12
                    }
                ]
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
