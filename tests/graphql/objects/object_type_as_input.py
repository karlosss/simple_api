from graphene_django.utils import GraphQLTestCase

from adapters.utils import generate
from adapters.graphql.graphql import GraphQLAdapter
from object.actions import Action
from object.fields import StringField, ObjectField, IntegerField
from object.object import Object
from tests.graphql_test_utils import get_graphql_url, remove_ws
from utils import AttrDict


def get(*args, **kwargs):
    print(kwargs)


def get_null(*args, **kwargs):
    print(kwargs)


class TestObject(Object):
    fields = {
        "int1": IntegerField(),
        "int2": IntegerField(),
    }


class Actions(Object):
    actions = {
        "get": Action(parameters={"id": ObjectField(TestObject)}, return_value=StringField(), exec_fn=get),
        "get_null": Action(parameters={"id": ObjectField(TestObject, nullable=True)}, return_value=StringField(), exec_fn=get_null)
    }


# TODO
# schema = generate(GraphQLAdapter, [Actions, TestObject])
