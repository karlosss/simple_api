from simple_api.adapters.graphql.graphql import GraphQLAdapter
from simple_api.adapters.utils import generate
from simple_api.django_object.django_object import DjangoObject

from .models import TestModelPrimitiveFields
from tests.graphql.graphql_test_utils import build_patterns


class TestModelObjectAllFields(DjangoObject):
    model = TestModelPrimitiveFields
    class_for_related = False
    detail_action = None
    update_action = None
    delete_action = None
    list_action = None


class TestModelObjectOnlyFields(DjangoObject):
    model = TestModelPrimitiveFields
    only_fields = ("int_field", "float_field")
    detail_action = None
    update_action = None
    delete_action = None
    list_action = None


class TestModelObjectExcludeFields(DjangoObject):
    model = TestModelPrimitiveFields
    class_for_related = False
    exclude_fields = ("string_char_field", "string_text_field")
    detail_action = None
    update_action = None
    delete_action = None
    list_action = None


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
