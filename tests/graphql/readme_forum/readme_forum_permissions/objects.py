from django.contrib.auth.models import User as UserModel

from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.actions import CreateAction, UpdateAction, DeleteAction, DetailAction, ListAction, ModelAction
from simple_api.django_object.django_object import DjangoObject
from simple_api.django_object.permissions import IsAuthenticated
from simple_api.object.datatypes import StringType
from simple_api.object.permissions import Or

from simple_api.adapters.graphql.utils import build_patterns

from .models import Post as PostModel


class IsAdmin(IsAuthenticated):
    def permission_statement(self, request, obj, **kwargs):
        return request.user.is_staff or request.user.is_superuser


class IsSelf(IsAuthenticated):
    def permission_statement(self, request, obj, **kwargs):
        return request.user == obj


class IsTheirs(IsAuthenticated):
    def permission_statement(self, request, obj, **kwargs):
        return request.user == obj.author


def set_password(request, params, **kwargs):
    # this would set a password to request.user, but for the showcase it is not needed
    pass


def create_post(request, params, **kwargs):
    data = params["data"]
    return PostModel.objects.create(title=data["title"], content=data["content"], author=request.user)


class User(DjangoObject):
    model = UserModel
    only_fields = ("username", )

    create_action = CreateAction(permissions=IsAdmin)
    update_action = UpdateAction(permissions=IsAdmin)
    delete_action = DeleteAction(permissions=IsAdmin)
    detail_action = DetailAction(permissions=IsAdmin)
    list_action = ListAction(permissions=IsAdmin)

    custom_actions = {
        "changePassword": ModelAction(data={"password": StringType()}, exec_fn=set_password,
                                      permissions=IsAuthenticated),
        "myProfile": ModelAction(exec_fn=lambda request, **kwargs: request.user, permissions=IsAuthenticated)
    }


class Post(DjangoObject):
    model = PostModel

    create_action = CreateAction(exclude_fields=("author_id",), permissions=IsAuthenticated, exec_fn=create_post)
    update_action = UpdateAction(permissions=Or(IsAdmin, IsTheirs))
    delete_action = DeleteAction(permissions=Or(IsAdmin, IsTheirs))
    list_action = ListAction(permissions=IsAuthenticated)
    detail_action = DetailAction(permissions=IsAuthenticated)


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
