from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from object.datatypes import StringType, ObjectType
from .models import CustomUser as CustomUserModel, Post as PostModel
from tests.graphql.graphql_test_utils import build_patterns


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
