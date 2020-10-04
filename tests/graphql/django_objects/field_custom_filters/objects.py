from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from django_object.filters import integer_filters
from object.datatypes import ObjectType
from .models import Person, Car
from tests.graphql.graphql_test_utils import build_patterns


class PersonObject(DjangoObject):
    model = Person


class CarObject(DjangoObject):
    model = Car
    output_custom_fields = {
        "owner": ObjectType(PersonObject, custom_filters=integer_filters("owner__age"))
    }


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
