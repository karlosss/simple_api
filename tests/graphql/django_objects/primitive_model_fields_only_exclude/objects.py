from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from .models import TestModelPrimitiveFields
from tests.graphql.graphql_test_utils import build_patterns


class TestModelObjectAllFields(DjangoObject):
    model = TestModelPrimitiveFields
    class_for_related = False


class TestModelObjectOnlyFields(DjangoObject):
    model = TestModelPrimitiveFields
    only_fields = ("int_field", "float_field")


class TestModelObjectExcludeFields(DjangoObject):
    model = TestModelPrimitiveFields
    class_for_related = False
    exclude_fields = ("string_char_field", "string_text_field")


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)