from collections import OrderedDict
from functools import singledispatch

from django_object.datatypes import PaginatedList
from object.datatypes import IntegerType, PlainListType, BooleanType, StringType, ObjectType
from utils import Storage


def build_filters_for_field(filters, field_name):
    out = OrderedDict()
    for filter_name, filter in filters.items():
        key = "{}{}{}".format(field_name, "__" if filter_name else "", filter_name)
        out[key] = filter
    return out


def string_filters(field_name):
    return build_filters_for_field(OrderedDict({
        "": StringType(nullable=True),
        "contains": StringType(nullable=True),
        "endswith": StringType(nullable=True),
        "exact": StringType(nullable=True),
        "icontains": StringType(nullable=True),
        "in": PlainListType(StringType(), nullable=True),
        "iregex": StringType(nullable=True),
        "isnull": BooleanType(nullable=True),
        "regex": StringType(nullable=True),
        "startswith": StringType(nullable=True),
    }), field_name)


def integer_filters(field_name):
    return build_filters_for_field(OrderedDict({
        "": IntegerType(nullable=True),
        "exact": IntegerType(nullable=True),
        "gt": IntegerType(nullable=True),
        "gte": IntegerType(nullable=True),
        "in": PlainListType(IntegerType(), nullable=True),
        "isnull": BooleanType(nullable=True),
        "lt": IntegerType(nullable=True),
        "lte": IntegerType(nullable=True),
    }), field_name)


@singledispatch
def determine_filters_for_type(type, field_name):
    return OrderedDict()


@determine_filters_for_type.register(IntegerType)
def determine_filters_for_integer(type, field_name):
    return integer_filters(field_name)


@determine_filters_for_type.register(StringType)
def determine_filters_for_string(type, field_name):
    return string_filters(field_name)


@determine_filters_for_type.register(ObjectType)
def determine_filters_for_object(type, field_name):
    return integer_filters(field_name + "_id")


@determine_filters_for_type.register(PaginatedList)
def determine_filters_for_object(type, field_name):
    return OrderedDict()


def determine_filters(cls):
    filters = OrderedDict()
    for name, field in cls.out_fields.items():
        if field.kwargs.get("generate_filters", True):
            filters.update(determine_filters_for_type(field, name))
    return filters


class ModelFiltersStorage(Storage):
    def store(self, model, cls):
        self.get(model)
        filters = determine_filters(cls)
        self.storage[model].update(filters)

    def get(self, model):
        if model not in self.storage:
            self.storage[model] = OrderedDict()
        return self.storage[model]


model_filters_storage = ModelFiltersStorage()
