from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from .models import CustomUser as CustomUserModel, Post as PostModel
from tests.graphql.graphql_test_utils import build_patterns


class CustomUser(DjangoObject):
    model = CustomUserModel
    class_for_related = False


class CustomUserPublic(DjangoObject):
    model = CustomUserModel
    exclude_fields = ("email", "password")


class Post(DjangoObject):
    model = PostModel


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
