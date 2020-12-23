from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from object.datatypes import StringType
from .models import CustomUser as CustomUserModel, Post as PostModel
from tests.graphql.graphql_test_utils import build_patterns


class ShortCustomUser(DjangoObject):
    model = CustomUserModel
    only_fields = ("first_name", "last_name")
    output_custom_fields = {"full_name": StringType()}


class ShortPost(DjangoObject):
    model = PostModel
    exclude_fields = ("content",)


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
