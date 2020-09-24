from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import IntegerType, ObjectType, StringType
from object.function import Function
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns


def get(request, params):
    if "id" in params:
        return "{}.{}".format(params["id"]["int1"], params["id"]["int2"])
    return "no params passed"


class TestObject(Object):
    fields = {
        "int1": IntegerType(),
        "int2": IntegerType(),
    }


actions = {
    "get": Action(parameters={"id": ObjectType(TestObject)}, return_value=StringType(), exec_fn=Function(get)),
    "get_null": Action(parameters={"id": ObjectType(TestObject, nullable=True)}, return_value=StringType(), exec_fn=Function(get)),
    "get_null_default": Action(parameters={"id": ObjectType(TestObject, nullable=True, default={"int1": 10, "int2": 20})},
                               return_value=StringType(), exec_fn=Function(get))
}


schema = generate(GraphQLAdapter, actions)
patterns = build_patterns(schema)
