from functools import singledispatch

import graphene

from adapters.graphql.registry import get_class
from adapters.graphql.utils import ConversionType
from object.datatypes import StringType, IntegerType, ObjectType, PlainListType, BooleanType, FloatType, DateType, \
    TimeType, DateTimeType


@singledispatch
def convert_list_output_type(type, adapter, **kwargs):
    raise NotImplementedError(type.__class__)


@convert_list_output_type.register(StringType)
def convert_list_output_string_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.String
    return graphene.NonNull(graphene.String)


@convert_list_output_type.register(IntegerType)
def convert_list_output_integer_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.Int
    return graphene.NonNull(graphene.Int)


@convert_list_output_type.register(BooleanType)
def convert_list_output_boolean_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.Boolean
    return graphene.NonNull(graphene.Boolean)


@convert_list_output_type.register(FloatType)
def convert_list_output_float_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.Float
    return graphene.NonNull(graphene.Float)


@convert_list_output_type.register(DateType)
def convert_list_output_date_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.Date
    return graphene.NonNull(graphene.Date)


@convert_list_output_type.register(TimeType)
def convert_list_output_time_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.Time
    return graphene.NonNull(graphene.Time)


@convert_list_output_type.register(DateTimeType)
def convert_list_output_date_time_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.DateTime
    return graphene.NonNull(graphene.DateTime)


@convert_list_output_type.register(ObjectType)
def convert_list_output_object_type(type, adapter, **kwargs):
    if type.nullable():
        return get_class(type.to)
    return graphene.NonNull(get_class(type.to))


@convert_list_output_type.register(PlainListType)
def convert_list_output_list_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.List(type.of.convert(adapter, _as=ConversionType.LIST_OUTPUT))
    return graphene.NonNull(graphene.List(type.of.convert(adapter, _as=ConversionType.LIST_OUTPUT)))
