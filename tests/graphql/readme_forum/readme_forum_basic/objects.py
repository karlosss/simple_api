from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject

from tests.graphql.graphql_test_utils import build_patterns

from .models import CustomUser as CustomUserModel, Post as PostModel


class CustomUser(DjangoObject):
    model = CustomUserModel


class Post(DjangoObject):
    model = PostModel


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
