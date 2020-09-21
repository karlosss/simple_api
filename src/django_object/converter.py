from functools import singledispatch
from inspect import isclass

from django.db.models import AutoField, IntegerField, CharField, TextField, BooleanField, FloatField, DateField, \
    TimeField, DateTimeField, ForeignKey, ManyToOneRel, Model

from django_object.registry import django_object_meta_storage
from object.datatypes import IntegerType, StringType, BooleanType, FloatType, DateType, TimeType, DateTimeType, \
    ObjectType, PlainListType


def model_set_ref_handler(object_type):
    if isclass(object_type.to) and issubclass(object_type.to, Model):
        object_type.to = django_object_meta_storage.get_class(object_type.to)


@singledispatch
def convert_django_field(field):
    raise NotImplementedError(field.__class__)


@convert_django_field.register(AutoField)
@convert_django_field.register(IntegerField)
def convert_to_integer_type(field):
    return IntegerType(nullable=field.null)


@convert_django_field.register(CharField)
@convert_django_field.register(TextField)
def convert_to_string_type(field):
    return StringType(nullable=field.null)


@convert_django_field.register(BooleanField)
def convert_to_boolean_type(field):
    return BooleanType(nullable=field.null)


@convert_django_field.register(FloatField)
def convert_to_float_type(field):
    return FloatType(nullable=field.null)


@convert_django_field.register(DateField)
def convert_to_date_type(field):
    return DateType(nullable=field.null)


@convert_django_field.register(TimeField)
def convert_to_time_type(field):
    return TimeType(nullable=field.null)


@convert_django_field.register(DateTimeField)
def convert_to_date_time_type(field):
    return DateTimeType(nullable=field.null)


@convert_django_field.register(ForeignKey)
def convert_to_object_type(field):
    target_model = field.remote_field.model
    type = ObjectType(target_model, nullable=field.null)
    type._set_ref_handler = model_set_ref_handler
    return type


@convert_django_field.register(ManyToOneRel)
def convert_to_list_of_object_type(field):
    target_model = field.remote_field.model
    type = ObjectType(target_model)
    type._set_ref_handler = model_set_ref_handler
    return PlainListType(type)
