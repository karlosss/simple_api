from functools import singledispatch

import graphene

from adapters.graphql.converter.datatypes import Duration
from adapters.graphql.registry import get_class
from adapters.graphql.utils import ConversionType
from object.datatypes import StringType, IntegerType, ObjectType, PlainListType, BooleanType, FloatType, DateType, \
    TimeType, DateTimeType, DurationType


@singledispatch
def convert_output_type(type, adapter, **kwargs):
    raise NotImplementedError(type.__class__)


@convert_output_type.register(StringType)
def convert_output_string_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.String, adapter, **kwargs)


@convert_output_type.register(IntegerType)
def convert_output_integer_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.Int, adapter, **kwargs)


@convert_output_type.register(BooleanType)
def convert_output_boolean_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.Boolean, adapter, **kwargs)


@convert_output_type.register(FloatType)
def convert_output_float_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.Float, adapter, **kwargs)


@convert_output_type.register(DateType)
def convert_output_date_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.Date, adapter, **kwargs)


@convert_output_type.register(TimeType)
def convert_output_time_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.Time, adapter, **kwargs)


@convert_output_type.register(DateTimeType)
def convert_output_date_time_type(type, adapter, **kwargs):
    return convert_output_class_type(type, graphene.DateTime, adapter, **kwargs)


@convert_output_type.register(DurationType)
def convert_output_duration_type(type, adapter, **kwargs):
    return convert_output_class_type(type, Duration, adapter, **kwargs)


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
    kwargs["resolver"] = kwargs.get("resolver", type.resolver.convert(adapter, _as=ConversionType.RESOLVER))
    return graphene.Field(cls,
                          required=not type.nullable(),
                          default_value=type.default(),
                          **kwargs)
