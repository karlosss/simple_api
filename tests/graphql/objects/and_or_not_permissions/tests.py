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
          allow1: Boolean!
          allow2: Boolean!
          allow3: Boolean!
          allow4: Boolean!
          allow5: Boolean!
          deny1: Boolean!
          deny2: Boolean!
          deny3: Boolean!
          deny4: Boolean!
          deny5: Boolean!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TypeInfo {
          typename: String!
          fields: [FieldInfo!]!
          __str__: String!
        }"""

    REF_META_SCHEMA = {
        "data": {
            "__types": [],
            "__objects": [],
            "__actions": [
                {
                    "name": "allow1",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "allow2",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "allow3",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "allow4",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "allow5",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "deny1",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": False,
                    "deny_reason": "You do not have permission to access this.",
                    "retry_in": None
                },
                {
                    "name": "deny2",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": False,
                    "deny_reason": "You do not have permission to access this.",
                    "retry_in": None
                },
                {
                    "name": "deny3",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": False,
                    "deny_reason": "You do not have permission to access this.",
                    "retry_in": None
                },
                {
                    "name": "deny4",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": False,
                    "deny_reason": "You do not have permission to access this.",
                    "retry_in": None
                },
                {
                    "name": "deny5",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Boolean!",
                    "permitted": False,
                    "deny_reason": "You do not have permission to access this.",
                    "retry_in": None
                }
            ]
        }
    }

    def test_allow1(self):
        resp = self.query(
            """
            query{
              allow1
            }
            """
        )

        exp = {
            "data": {
                "allow1": True
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_allow2(self):
        resp = self.query(
            """
            query{
              allow2
            }
            """
        )

        exp = {
            "data": {
                "allow2": True
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_allow3(self):
        resp = self.query(
            """
            query{
              allow3
            }
            """
        )

        exp = {
            "data": {
                "allow3": True
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_allow4(self):
        resp = self.query(
            """
            query{
              allow4
            }
            """
        )

        exp = {
            "data": {
                "allow4": True
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_allow5(self):
        resp = self.query(
            """
            query{
              allow5
            }
            """
        )

        exp = {
            "data": {
                "allow5": True
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_deny1(self):
        resp = self.query(
            """
            query{
              deny1
            }
            """
        )

        exp = {
            "errors": [
                {
                    "message": "You do not have permission to access this.",
                    "locations": [
                        {
                            "line": 3,
                            "column": 15
                        }
                    ],
                    "path": [
                        "deny1"
                    ]
                }
            ],
            "data": None
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_deny2(self):
        resp = self.query(
            """
            query{
              deny2
            }
            """
        )

        exp = {
            "errors": [
                {
                    "message": "You do not have permission to access this.",
                    "locations": [
                        {
                            "line": 3,
                            "column": 15
                        }
                    ],
                    "path": [
                        "deny2"
                    ]
                }
            ],
            "data": None
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_deny3(self):
        resp = self.query(
            """
            query{
              deny3
            }
            """
        )

        exp = {
            "errors": [
                {
                    "message": "You do not have permission to access this.",
                    "locations": [
                        {
                            "line": 3,
                            "column": 15
                        }
                    ],
                    "path": [
                        "deny3"
                    ]
                }
            ],
            "data": None
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_deny4(self):
        resp = self.query(
            """
            query{
              deny4
            }
            """
        )

        exp = {
            "errors": [
                {
                    "message": "You do not have permission to access this.",
                    "locations": [
                        {
                            "line": 3,
                            "column": 15
                        }
                    ],
                    "path": [
                        "deny4"
                    ]
                }
            ],
            "data": None
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)

    def test_deny5(self):
        resp = self.query(
            """
            query{
              deny5
            }
            """
        )

        exp = {
            "errors": [
                {
                    "message": "You do not have permission to access this.",
                    "locations": [
                        {
                            "line": 3,
                            "column": 15
                        }
                    ],
                    "path": [
                        "deny5"
                    ]
                }
            ],
            "data": None
        }

        self.assertResponseHasErrors(resp)
        self.assertJSONEqual(resp.content, exp)
