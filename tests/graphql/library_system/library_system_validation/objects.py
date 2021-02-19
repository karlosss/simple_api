from django.core.exceptions import ObjectDoesNotExist

from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject
from simple_api.object.actions import Action
from simple_api.object.datatypes import IntegerType, ObjectType, StringType
from simple_api.object.validators import Validator, And

from tests.graphql.graphql_test_utils import build_patterns

from .models import Book as BookModel, Bookmark as BookmarkModel


class NotNegative(Validator):
    def validation_statement(self, request, value=None, **kwargs):
        return value >= 0

    def error_message(self, **kwargs):
        return "Validation failed in NotNegative"


class NotZero(Validator):
    def validation_statement(self, request, value=None, **kwargs):
        return value != 0

    def error_message(self, **kwargs):
        return "Validation failed in NotZero"


class LongerThen3Characters(Validator):
    def validation_statement(self, request, value=None, **kwargs):
        return len(value) > 3

    def error_message(self, **kwargs):
        return "Search term must be at least 4 characters"


class NotRestrictedBook(Validator):
    def validation_statement(self, request, value=None, **kwargs):
        try:
            return not BookModel.objects.get(id=kwargs["params"]["id"]).restricted
        except ObjectDoesNotExist:
            return True

    def error_message(self, **kwargs):
        return "Only not restricted books can be accessed"


def get_by_id(**kwargs):
    return BookModel.objects.get(id=kwargs["params"]["id"])


class Book(DjangoObject):
    model = BookModel
    custom_actions = {
        "getById": Action(parameters={"id": IntegerType(validators=And(NotNegative, NotZero))},
                          return_value=ObjectType("self"),
                          validators=NotRestrictedBook,
                          exec_fn=get_by_id),
        "getById2": Action(parameters={"id": IntegerType(validators=NotNegative)},
                           data={"Title": StringType(validators=LongerThen3Characters)},
                           return_value=ObjectType("self"),
                           validators=NotRestrictedBook,
                           exec_fn=get_by_id)}


class Bookmark(DjangoObject):
    model = BookmarkModel


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
