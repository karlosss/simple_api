from django.contrib.auth import get_user_model

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object import DjangoObject
from object.actions import Action
from object.datatypes import StringType, IntegerType, ObjectType
from tests.graphql.graphql_test_utils import build_patterns
from utils import AttrDict

from .models import Car as CarModel


class Car(DjangoObject):
    model = CarModel


class User(DjangoObject):
    model = get_user_model()
    only_fields = ("username",)


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
