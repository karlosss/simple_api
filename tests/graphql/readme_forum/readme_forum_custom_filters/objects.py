from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject
from simple_api.object.datatypes import StringType, ObjectType

from tests.graphql.graphql_test_utils import build_patterns

from .models import CustomUser as CustomUserModel, Post as PostModel


class CustomUser(DjangoObject):
    model = CustomUserModel
    custom_fields = {
        "email": StringType(only_filters=("email__exact", "email__icontains")),
        "first_name": StringType(exclude_filters=("first_name__regex", "first_name__iregex")),
    }


class Post(DjangoObject):
    model = PostModel
    output_custom_fields = {
        "author": ObjectType(CustomUser, exclude_filters=(),
                             custom_filters={"author__email": StringType(nullable=True)})
    }


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
