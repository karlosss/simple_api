from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from object.datatypes import IntegerType, StringType
from .models import TestModel
from tests.graphql.graphql_test_utils import build_patterns


def hide_if_short(request, parent_val, params, **kwargs):
    if len(parent_val) < 3:
        return None
    return parent_val


class TestObject(DjangoObject):
    model = TestModel
    output_custom_fields = {
        "int_plus_one": IntegerType(nullable=False)
    }
    custom_fields = {
        "string_field": StringType(nullable=True, nullable_if_input=False,
                                   resolver=hide_if_short, exclude_filters=())
    }


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
