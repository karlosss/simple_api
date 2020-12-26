import datetime

from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import DateType, TimeType, DateTimeType, ObjectType
from simple_api.object.object import Object

from tests.graphql.graphql_test_utils import build_patterns


def get_object(request, params, **kwargs):
    return {
        "date": datetime.date(2020, 1, 1),
        "time": datetime.time(12, 34, 56),
        "datetime": datetime.datetime(2020, 1, 1, 12, 34, 56)
    }


def get_date(request, params, **kwargs):
    return datetime.date(2020, 1, 1)


def get_time(request, params, **kwargs):
    return datetime.time(12, 34, 56)


def get_datetime(request, params, **kwargs):
    return datetime.datetime(2020, 1, 1, 12, 34, 56)


def echo(request, params, **kwargs):
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
    "getObject": Action(return_value=ObjectType(TestObject), exec_fn=get_object),
    "getDate": Action(return_value=DateType(), exec_fn=get_date),
    "getTime": Action(return_value=TimeType(), exec_fn=get_time),
    "getDatetime": Action(return_value=DateTimeType(), exec_fn=get_datetime),
    "echo": Action(parameters={"date": DateType(), "time": TimeType(), "datetime": DateTimeType()},
                   return_value=ObjectType(TestObject), exec_fn=echo),
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
