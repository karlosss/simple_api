from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.actions import CreateAction, UpdateAction
from simple_api.django_object.django_object import DjangoObject

from tests.graphql.graphql_test_utils import build_patterns

from .models import CustomUser as CustomUserModel, Post as PostModel


def custom_create_user(request, params, **kwargs):
    return CustomUserModel.objects.create(
        email="default@example.com",
        username=params["data"]["username"],
        first_name="Name",
        last_name="Surname",
        password="default"
    )


class CustomUser(DjangoObject):
    model = CustomUserModel

    create_action = CreateAction(only_fields=("username",), exec_fn=custom_create_user)
    update_action = None
    delete_action = None

    custom_actions = {
        "changePassword": UpdateAction(only_fields=("password",), required_fields=("password",))
    }


class Post(DjangoObject):
    model = PostModel


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
