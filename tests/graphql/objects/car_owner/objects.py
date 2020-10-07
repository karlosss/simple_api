from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from object.actions import Action
from object.datatypes import StringType, IntegerType, ObjectType
from object.object import Object
from tests.graphql.graphql_test_utils import build_patterns
from utils import AttrDict


def get_by_id(request, params):
    return AttrDict(id=params["id"], car=AttrDict(model="BMW", color="blue"))


class Car(Object):
    fields = {
        "model": StringType(),
        "color": StringType()
    }


class Owner(Object):
    fields = {
        "id": IntegerType(),
        "car": ObjectType(Car)
    }

    actions = {
        "getById": Action(parameters={"id": IntegerType()}, return_value=ObjectType("self"), exec_fn=get_by_id)
    }


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
