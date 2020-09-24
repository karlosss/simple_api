import datetime

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import DateType, TimeType, DateTimeType, ObjectType
from object.function import Function
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns


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


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
