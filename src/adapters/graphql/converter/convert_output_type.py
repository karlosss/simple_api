from functools import singledispatch

import graphene

from adapters.graphql.registry import get_class
from object.datatypes import StringType, IntegerType, ObjectType, PlainListType


@singledispatch
def convert_output_type(type, adapter, **kwargs):
    raise NotImplementedError


@convert_output_type.register(StringType)
def convert_output_string_type(type, adapter, **kwargs):
    return graphene.Field(graphene.String, required=not type.nullable, default_value=type.default, **kwargs)


@convert_output_type.register(IntegerType)
def convert_output_integer_type(type, adapter, **kwargs):
    return graphene.Field(graphene.Int, required=not type.nullable, default_value=type.default, **kwargs)


@convert_output_type.register(ObjectType)
def convert_output_object_type(type, adapter, **kwargs):
    return graphene.Field(get_class(type.to).output, required=not type.nullable, default_value=type.default, **kwargs)


@convert_output_type.register(PlainListType)
def convert_output_list_type(type, adapter, **kwargs):
    return graphene.Field(graphene.List(type.of.convert(adapter, list=True)),
                          required=not type.nullable, default_value=type.default, **kwargs)
