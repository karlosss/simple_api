from functools import singledispatch

import graphene

from adapters.graphql.registry import get_class
from object.datatypes import StringType, IntegerType, ObjectType, PlainListType


@singledispatch
def convert_input_type(type, adapter, **kwargs):
    raise NotImplementedError


@convert_input_type.register(StringType)
def convert_input_string_type(type, adapter, **kwargs):
    return graphene.Argument(graphene.String, required=not type.nullable, default_value=type.default, **kwargs)


@convert_input_type.register(IntegerType)
def convert_input_integer_type(type, adapter, **kwargs):
    return graphene.Argument(graphene.Int, required=not type.nullable, default_value=type.default, **kwargs)


@convert_input_type.register(ObjectType)
def convert_input_object_type(type, adapter, **kwargs):
    return graphene.Argument(get_class(type.to).input, required=not type.nullable, default_value=type.default, **kwargs)


@convert_input_type.register(PlainListType)
def convert_input_list_type(type, adapter, **kwargs):
    return graphene.Argument(graphene.List(type.of.convert(adapter, list=True, input=True)),
                             required=not type.nullable, default_value=type.default, **kwargs)
