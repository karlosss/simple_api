from functools import singledispatch

import graphene

from adapters.graphql.registry import get_class
from adapters.graphql.utils import ConversionType
from object.datatypes import StringType, IntegerType, ObjectType, PlainListType, BooleanType, FloatType


@singledispatch
def convert_list_output_type(type, adapter, **kwargs):
    raise NotImplementedError


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
def convert_list_output_integer_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.Int
    return graphene.NonNull(graphene.Boolean)


@convert_list_output_type.register(FloatType)
def convert_list_output_integer_type(type, adapter, **kwargs):
    if type.nullable():
        return graphene.Int
    return graphene.NonNull(graphene.Float)


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
