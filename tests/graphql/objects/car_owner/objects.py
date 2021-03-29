from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.object.actions import Action
from simple_api.object.datatypes import StringType, IntegerType, ObjectType
from simple_api.object.object import Object
from simple_api.utils import AttrDict

from simple_api.adapters.graphql.utils import build_patterns


def get_by_id(request, params, **kwargs):
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
patterns = build_patterns("api/", schema)
