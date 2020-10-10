from functools import singledispatch

import graphene

from adapters.graphql.converter.datatypes import Duration
from adapters.graphql.registry import get_class
from adapters.graphql.utils import ConversionType
from object.datatypes import StringType, IntegerType, ObjectType, PlainListType, BooleanType, FloatType, DateType, \
    TimeType, DateTimeType, DurationType


@singledispatch
def convert_list_input_type(type, adapter, **kwargs):
    raise NotImplementedError(type.__class__)


@convert_list_input_type.register(StringType)
def convert_list_input_string_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return graphene.String
    return graphene.NonNull(graphene.String)


@convert_list_input_type.register(IntegerType)
def convert_list_input_integer_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return graphene.Int
    return graphene.NonNull(graphene.Int)


@convert_list_input_type.register(BooleanType)
def convert_list_input_boolean_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return graphene.Boolean
    return graphene.NonNull(graphene.Boolean)


@convert_list_input_type.register(FloatType)
def convert_list_input_float_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return graphene.Float
    return graphene.NonNull(graphene.Float)


@convert_list_input_type.register(DateType)
def convert_list_input_date_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return graphene.Date
    return graphene.NonNull(graphene.Date)


@convert_list_input_type.register(TimeType)
def convert_list_input_time_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return graphene.Time
    return graphene.NonNull(graphene.Time)


@convert_list_input_type.register(DateTimeType)
def convert_list_input_date_time_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return graphene.DateTime
    return graphene.NonNull(graphene.DateTime)


@convert_list_input_type.register(DurationType)
def convert_list_input_duration_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return Duration
    return graphene.NonNull(Duration)


@convert_list_input_type.register(ObjectType)
def convert_list_input_object_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return get_class(type.to, input=True)
    return graphene.NonNull(get_class(type.to, input=True))


@convert_list_input_type.register(PlainListType)
def convert_list_input_list_type(type, adapter, **kwargs):
    if type.nullable(input=True):
        return graphene.List(type.of.convert(adapter, _as=ConversionType.LIST_INPUT))
    return graphene.NonNull(graphene.List(type.of.convert(adapter, _as=ConversionType.LIST_INPUT)))
