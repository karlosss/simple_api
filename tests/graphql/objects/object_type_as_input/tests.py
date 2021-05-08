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
          get(id: TestObjectInput!): String!
          getNull(id: TestObjectInput): String!
          getNullDefault(id: TestObjectInput = {int1: 10, int2: 20}): String!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        input TestObjectInput {
          int1: Int!
          int2: Int!
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
                    "name": "get",
                    "parameters": [
                        {
                            "name": "id",
                            "typename": "TestObject!",
                            "default": None
                        }
                    ],
                    "data": [],
                    "mutation": False,
                    "return_type": "String!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getNull",
                    "parameters": [
                        {
                            "name": "id",
                            "typename": "TestObject",
                            "default": None
                        }
                    ],
                    "data": [],
                    "mutation": False,
                    "return_type": "String!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getNullDefault",
                    "parameters": [
                        {
                            "name": "id",
                            "typename": "TestObject",
                            "default": "{'int1': 10, 'int2': 20}"
                        }
                    ],
                    "data": [],
                    "mutation": False,
                    "return_type": "String!",
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
              get(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
            "data": {
                "get": "1.2"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_non_null_fail(self):
        resp = self.query(
            """
            query{
              get
            }
            """
        )

        self.assertResponseHasErrors(resp)

    def test_request_null_param(self):
        resp = self.query(
            """
            query{
              getNull(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
            "data": {
                "getNull": "1.2"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_no_param(self):
        resp = self.query(
            """
            query{
              getNull
            }
            """
        )

        exp = {
            "data": {
                "getNull": "no params passed"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_default_no_param(self):
        resp = self.query(
            """
            query{
              getNullDefault
            }
            """
        )

        exp = {
            "data": {
                "getNullDefault": "10.20"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_request_null_default_with_param(self):
        resp = self.query(
            """
            query{
              getNullDefault(id: {int1: 1, int2: 2})
            }
            """
        )

        exp = {
            "data": {
                "getNullDefault": "1.2"
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
