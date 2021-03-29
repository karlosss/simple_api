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
        
        scalar Date
        
        scalar DateTime
        
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
          getObject: TestObject!
          getDate: Date!
          getTime: Time!
          getDatetime: DateTime!
          echo(date: Date!, time: Time!, datetime: DateTime!): TestObject!
          __types: [TypeInfo!]!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          date: Date!
          time: Time!
          datetime: DateTime!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        scalar Time
        
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
                            "name": "date",
                            "typename": "Date!"
                        },
                        {
                            "name": "time",
                            "typename": "Time!"
                        },
                        {
                            "name": "datetime",
                            "typename": "DateTime!"
                        }
                    ]
                }
            ],
            "__objects": [],
            "__actions": [
                {
                    "name": "getObject",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "TestObject!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getDate",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Date!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getTime",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "Time!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "getDatetime",
                    "parameters": [],
                    "data": [],
                    "mutation": False,
                    "return_type": "DateTime!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                },
                {
                    "name": "echo",
                    "parameters": [
                        {
                            "name": "date",
                            "typename": "Date!",
                            "default": None
                        },
                        {
                            "name": "time",
                            "typename": "Time!",
                            "default": None
                        },
                        {
                            "name": "datetime",
                            "typename": "DateTime!",
                            "default": None
                        }
                    ],
                    "data": [],
                    "mutation": False,
                    "return_type": "TestObject!",
                    "permitted": True,
                    "deny_reason": None,
                    "retry_in": None
                }
            ]
        }
    }

    def test_request(self):
        resp = self.query(
            """
            query {
              getObject{
                date
                time
                datetime
              }
              getDate
              getTime
              getDatetime
              echo(date: "2020-01-01", time: "12:34:56", datetime: "2020-01-01T12:34:56"){
                date
                time
                datetime
              }
            }
            """
        )

        exp = {
            "data": {
                "getObject": {
                    "date": "2020-01-01",
                    "time": "12:34:56",
                    "datetime": "2020-01-01T12:34:56"
                },
                "getDate": "2020-01-01",
                "getTime": "12:34:56",
                "getDatetime": "2020-01-01T12:34:56",
                "echo": {
                    "date": "2020-01-01",
                    "time": "12:34:56",
                    "datetime": "2020-01-01T12:34:56"
                }
            }
        }

        self.assertResponseNoErrors(resp)
        self.assertJSONEqual(resp.content, exp)
