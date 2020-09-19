import datetime

from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.datatypes import ObjectType, DateType, TimeType, DateTimeType
from object.function import Function
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws


def get_object(request, params):
    return {
        "date": datetime.date(2020, 1, 1),
        "time": datetime.time(12, 34, 56),
        "datetime": datetime.datetime(2020, 1, 1, 12, 34, 56)
    }


def get_date(request, params):
    return datetime.date(2020, 1, 1)


def get_time(request, params):
    return datetime.time(12, 34, 56)


def get_datetime(request, params):
    return datetime.datetime(2020, 1, 1, 12, 34, 56)


def echo(request, params):
    return {
        "date": params.get("date"),
        "time": params.get("time"),
        "datetime": params.get("datetime")
    }


class TestObject(Object):
    fields = {
        "date": DateType(),
        "time": TimeType(),
        "datetime": DateTimeType(),
    }


actions = {
    "get_object": Action(return_value=ObjectType(TestObject), exec_fn=Function(get_object)),
    "get_date": Action(return_value=DateType(), exec_fn=Function(get_date)),
    "get_time": Action(return_value=TimeType(), exec_fn=Function(get_time)),
    "get_datetime": Action(return_value=DateTimeType(), exec_fn=Function(get_datetime)),
    "echo": Action(parameters={"date": DateType(), "time": TimeType(), "datetime": DateTimeType()},
                   return_value=ObjectType(TestObject), exec_fn=Function(echo)),
}

schema = generate(GraphQLAdapter, [TestObject], actions)


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = get_graphql_url(__file__)

    def test_schema(self):
        self.assertEqual(
            remove_ws(str(self.GRAPHQL_SCHEMA)),
            remove_ws(
                """
                schema {
                  query: Query
                }
                
                scalar Date
                
                scalar DateTime
                
                type Query {
                  getObject: TestObject!
                  getDate: Date!
                  getTime: Time!
                  getDatetime: DateTime!
                  echo(date: Date!, time: Time!, datetime: DateTime!): TestObject!
                }
                
                type TestObject {
                  date: Date!
                  time: Time!
                  datetime: DateTime!
                }
                
                scalar Time
                """
            )
        )

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
