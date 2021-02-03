from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject
from simple_api.django_object.permissions import IsAuthenticated, BasePermission
from simple_api.django_object.actions import CreateAction, UpdateAction, DeleteAction, DetailAction, ListAction, \
    ModelAction
from simple_api.object.datatypes import IntegerType

from tests.graphql.graphql_test_utils import build_patterns

from .models import Book as BookModel, Subscription as SubscriptionModel
from django.contrib.auth.models import User as UserModel


class IsAdmin(IsAuthenticated):
    def permission_statement(self, request, obj, **kwargs):
        return request.user.is_staff or request.user.is_superuser


class IsNotRestricted(BasePermission):
    def permission_statement(self, request, obj, **kwargs):
        return not obj.restricted

    def error_message(self, **kwargs):
        return "Restricted books cannot be borrowed."


def lend_book(request, params, **kwargs):
    data = params["data"]


class Book(DjangoObject):
    model = BookModel
    create_action = CreateAction()
    update_action = UpdateAction()
    delete_action = DeleteAction(permissions=IsAdmin)
    custom_actions = {
        "Lend": UpdateAction(exec_fn=lend_book,
                             permissions=IsNotRestricted),
    }


class Subscription(DjangoObject):
    model = SubscriptionModel


class User(DjangoObject):
    model = UserModel
    only_fields = ("username",)

    create_action = CreateAction(permissions=IsAdmin)
    update_action = UpdateAction(permissions=IsAdmin)
    delete_action = DeleteAction(permissions=IsAdmin)
    detail_action = DetailAction(permissions=IsAdmin)
    list_action = ListAction(permissions=IsAdmin)


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
