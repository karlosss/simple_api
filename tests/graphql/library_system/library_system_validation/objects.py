from django.core.exceptions import ObjectDoesNotExist

from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject
from simple_api.object.actions import Action
from simple_api.object.datatypes import IntegerType, ObjectType
from simple_api.object.validators import FieldValidator, ActionValidator

from tests.graphql.graphql_test_utils import build_patterns

from .models import Book as BookModel


class NotNegative(FieldValidator):
    def validation_statement(self, value, **kwargs):
        return value >= 0

    def error_message(self, **kwargs):
        return "Validation failed in NotNegative"


class NotZero(FieldValidator):
    def validation_statement(self, value, **kwargs):
        return value != 0

    def error_message(self, **kwargs):
        return "Validation failed in NotZero"


class ExistingNotRestrictedBook(ActionValidator):
    def validation_statement(self, **kwargs):
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
        "getById": Action(parameters={"id": IntegerType(validators=(NotNegative, NotZero))},
                          return_value=ObjectType("self"),
                          validators=ExistingNotRestrictedBook,
                          exec_fn=get_by_id),
        "getById2": Action(parameters={"id": IntegerType(validators=NotNegative)},
                           return_value=ObjectType("self"),
                           validators=ExistingNotRestrictedBook,
                           exec_fn=get_by_id)}


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
