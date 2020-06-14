from functools import singledispatch

import graphene

from adapters.graphql.registry import get_class
from adapters.graphql.utils import ConversionType
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
    return convert_output_class_type(type,
                                     get_class(type.to),
                                     adapter,
                                     **kwargs)


@convert_output_type.register(PlainListType)
def convert_output_list_type(type, adapter, **kwargs):
    return convert_output_class_type(type,
                                     graphene.List(type.of.convert(adapter, _as=ConversionType.LIST_OUTPUT)),
                                     adapter,
                                     **kwargs)


def convert_output_class_type(type, cls, adapter, **kwargs):
    kwargs["args"] = kwargs.get("args", {name: param.convert(adapter, _as=ConversionType.PARAMETER)
                                         for name, param in type.parameters.items()})
    kwargs["resolver"] = kwargs.get("resolver", type.resolver.convert(adapter, _as=ConversionType.RESOLVER)
                                                if type.resolver is not None else None)
    return graphene.Field(cls,
                          required=not type.nullable(),
                          default_value=type.default(),
                          **kwargs)
