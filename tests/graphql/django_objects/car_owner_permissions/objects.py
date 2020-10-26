from django.contrib.auth import get_user_model

from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object import DjangoObject
from django_object.actions import CreateAction
from object.actions import Action
from object.datatypes import StringType, IntegerType, ObjectType
from object.permissions import AllowAll
from tests.graphql.graphql_test_utils import build_patterns
from .permissions import IsAdmin

from .models import Car as CarModel


class Car(DjangoObject):
    model = CarModel


class User(DjangoObject):
    model = get_user_model()
    only_fields = ("username",)
    default_actions_permission = IsAdmin


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
