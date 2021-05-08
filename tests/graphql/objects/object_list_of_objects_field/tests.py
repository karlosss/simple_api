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
          getNonNull: [TestObject!]!
          getNull: [TestObject]
          getListNullElemNonNull: [TestObject!]
          getListNonNullElemNull: [TestObject]!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          int1: Int!
          int2: Int!
          __str__: String!
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
                    "typename": "TestObject",
                    "fields": [
                        {
                            "name": "int1",
                            "typename": "Integer!"
                        },
                        {
                            "name": "int2",
                            "typename": "Integer!"
                        }
                    ]
                }
            ],
            "__objects": [],
            "__actions": [
                {
                    "name": "getNonNull",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[TestObject!]!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getNull",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[TestObject]",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getListNullElemNonNull",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[TestObject!]",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getListNonNullElemNull",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "[TestObject]!",
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
