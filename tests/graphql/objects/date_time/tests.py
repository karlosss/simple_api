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
        
        scalar Date
        
        scalar DateTime
        
        scalar Duration
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Query {
          getObject: TestObject!
          getDate: Date!
          getTime: Time!
          getDatetime: DateTime!
          echo(date: Date!, time: Time!, datetime: DateTime!): TestObject!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type TestObject {
          date: Date!
          time: Time!
          datetime: DateTime!
          __actions: [ActionInfo!]!
        }
        
        scalar Time
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
            "name": "getObject",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          },
          {
            "name": "getDate",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          },
          {
            "name": "getTime",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          },
          {
            "name": "getDatetime",
            "permitted": True,
            "deny_reason": None,
            "retry_in": None
          },
          {
            "name": "echo",
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
