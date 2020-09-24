from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from .models import TestModelFKSource, TestModelFKTarget
from tests.graphql.graphql_test_utils import build_patterns


class FKSource(DjangoObject):
    model = TestModelFKSource


class FKTarget(DjangoObject):
    model = TestModelFKTarget


class FkTarget2(DjangoObject):
    model = TestModelFKTarget
    class_for_related = False


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
