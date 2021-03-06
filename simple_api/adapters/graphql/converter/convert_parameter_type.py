from functools import singledispatch

import graphene

from simple_api.adapters.graphql.converter.datatypes import Duration
from simple_api.adapters.graphql.registry import get_class
from simple_api.adapters.graphql.utils import ConversionType
from simple_api.object.datatypes import StringType, IntegerType, ObjectType, PlainListType, BooleanType, FloatType, DateType, \
    TimeType, DateTimeType, DurationType


@singledispatch
def convert_parameter_type(type, adapter, **kwargs):
    raise NotImplementedError(type.__class__)


@convert_parameter_type.register(StringType)
def convert_parameter_string_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type, graphene.String, adapter, **kwargs)


@convert_parameter_type.register(IntegerType)
def convert_parameter_integer_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type, graphene.Int, adapter, **kwargs)


@convert_parameter_type.register(BooleanType)
def convert_parameter_boolean_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type, graphene.Boolean, adapter, **kwargs)


@convert_parameter_type.register(FloatType)
def convert_parameter_float_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type, graphene.Float, adapter, **kwargs)


@convert_parameter_type.register(DateType)
def convert_parameter_date_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type, graphene.Date, adapter, **kwargs)


@convert_parameter_type.register(TimeType)
def convert_parameter_time_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type, graphene.Time, adapter, **kwargs)


@convert_parameter_type.register(DateTimeType)
def convert_parameter_date_time_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type, graphene.DateTime, adapter, **kwargs)


@convert_parameter_type.register(DurationType)
def convert_parameter_duration_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type, Duration, adapter, **kwargs)


@convert_parameter_type.register(ObjectType)
def convert_parameter_object_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type,
                                        get_class(type.to, input=True),
                                        adapter,
                                        **kwargs)


@convert_parameter_type.register(PlainListType)
def convert_parameter_list_type(type, adapter, **kwargs):
    return convert_parameter_class_type(type,
                                        graphene.List(type.of.convert(adapter, _as=ConversionType.LIST_INPUT)),
                                        adapter,
                                        **kwargs)


def convert_parameter_class_type(type, cls, adapter, **kwargs):
    return graphene.Argument(cls,
                             required=not type.nullable(input=True),
                             default_value=type.default(input=True),
                             **kwargs)
