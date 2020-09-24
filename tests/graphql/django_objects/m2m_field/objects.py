from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from .models import TestModelM2MSource, TestModelM2MTarget
from tests.graphql.graphql_test_utils import build_patterns


class M2MSource(DjangoObject):
    model = TestModelM2MSource


class M2MTarget(DjangoObject):
    model = TestModelM2MTarget


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
