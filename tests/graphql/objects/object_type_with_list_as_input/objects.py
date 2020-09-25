from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, ObjectType, StringType, PlainListType
from object.function import Function
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns
from utils import AttrDict


def resolve(request, parent_val, params):
    return parent_val["records"][params["offset"]:(params["offset"] + params["limit"])]


class Person(Object):
    fields = {
        "name": StringType(),
        "age": IntegerType(),
    }


class PersonList(Object):
    output_fields = {
        "count": IntegerType(),
    }
    fields = {
        "records": PlainListType(
            ObjectType(Person),
            parameters={
                "limit": IntegerType(nullable=True, default=20),
                "offset": IntegerType(nullable=True, default=0),
            },
            resolver=Function(resolve)
        )
    }


def get(request, params):
    return AttrDict(count=len(params["data"]), records=params["data"])


actions = {
    "get": Action({"data": ObjectType(PersonList)}, ObjectType(PersonList), Function(get))
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
