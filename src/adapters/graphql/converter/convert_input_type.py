from functools import singledispatch

import graphene

from adapters.graphql.registry import get_class
from adapters.graphql.utils import ConversionType
from object.datatypes import StringType, IntegerType, ObjectType, PlainListType, BooleanType, FloatType, DateType, \
    TimeType, DateTimeType


@singledispatch
def convert_input_type(type, adapter, **kwargs):
    raise NotImplementedError(type.__class__)


@convert_input_type.register(StringType)
def convert_input_string_type(type, adapter, **kwargs):
    return convert_input_class_type(type, graphene.String, adapter, **kwargs)


@convert_input_type.register(IntegerType)
def convert_input_integer_type(type, adapter, **kwargs):
    return convert_input_class_type(type, graphene.Int, adapter, **kwargs)


@convert_input_type.register(BooleanType)
def convert_input_boolean_type(type, adapter, **kwargs):
    return convert_input_class_type(type, graphene.Boolean, adapter, **kwargs)


@convert_input_type.register(FloatType)
def convert_input_float_type(type, adapter, **kwargs):
    return convert_input_class_type(type, graphene.Float, adapter, **kwargs)


@convert_input_type.register(DateType)
def convert_input_date_type(type, adapter, **kwargs):
    return convert_input_class_type(type, graphene.Date, adapter, **kwargs)


@convert_input_type.register(TimeType)
def convert_input_time_type(type, adapter, **kwargs):
    return convert_input_class_type(type, graphene.Time, adapter, **kwargs)


@convert_input_type.register(DateTimeType)
def convert_input_date_time_type(type, adapter, **kwargs):
    return convert_input_class_type(type, graphene.DateTime, adapter, **kwargs)


@convert_input_type.register(ObjectType)
def convert_input_object_type(type, adapter, **kwargs):
    return convert_input_class_type(type, get_class(type.to, input=True), adapter, **kwargs)


@convert_input_type.register(PlainListType)
def convert_input_list_type(type, adapter, **kwargs):
    return convert_input_class_type(type,
                                    graphene.List(type.of.convert(adapter, _as=ConversionType.LIST_INPUT)),
                                    adapter,
                                    **kwargs)


def convert_input_class_type(type, cls, adapter, **kwargs):
    return graphene.InputField(cls,
                               required=not type.nullable(input=True),
                               default_value=type.default(input=True),
                               **kwargs)
