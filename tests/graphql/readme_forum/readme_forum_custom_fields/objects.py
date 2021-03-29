from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject
from simple_api.object.datatypes import StringType

from simple_api.adapters.graphql.utils import build_patterns

from .models import CustomUser as CustomUserModel, Post as PostModel


class ShortCustomUser(DjangoObject):
    model = CustomUserModel
    only_fields = ("first_name", "last_name")
    output_custom_fields = {"full_name": StringType()}


class ShortPost(DjangoObject):
    model = PostModel
    exclude_fields = ("content",)


schema = generate(GraphQLAdapter)
patterns = build_patterns("api/", schema)
