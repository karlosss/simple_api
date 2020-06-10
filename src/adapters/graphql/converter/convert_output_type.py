from functools import singledispatch

import graphene

from adapters.graphql.registry import get_class
from object.datatypes import StringType, IntegerType, ObjectType, PlainListType


@singledispatch
def convert_output_type(type, adapter, **kwargs):
    raise NotImplementedError


@convert_output_type.register(StringType)
def convert_output_string_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.String, adapter, **kwargs)


@convert_output_type.register(IntegerType)
def convert_output_integer_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.Int, adapter, **kwargs)


@convert_output_type.register(ObjectType)
def convert_output_object_type(type, adapter, **kwargs):
    return convert_output_class_type(type, get_class(type.to).output, adapter, **kwargs)


@convert_output_type.register(PlainListType)
def convert_output_list_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.List(type.of.convert(adapter, list=True)), adapter, **kwargs)


def convert_output_class_type(type, cls, adapter, **kwargs):
    return graphene.Field(cls,
                          required=not type.nullable,
                          default_value=type.default,
                          args={name: field.convert(adapter, input=True, **kwargs)
                                for name, field in type.parameters.items()},
                          resolver=type.resolver.convert(adapter, resolver=True) if type.resolver is not None else None,
                          **kwargs)
