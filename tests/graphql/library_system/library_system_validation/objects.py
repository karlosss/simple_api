from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject

from tests.graphql.graphql_test_utils import build_patterns

from .models import Book as BookModel


class Book(DjangoObject):
    model = BookModel


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
