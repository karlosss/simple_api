from collections import OrderedDict
from functools import singledispatch

from django.db.models import AutoField, IntegerField, CharField, TextField, BooleanField, FloatField, DateField, \
    TimeField, DateTimeField, ForeignKey, ManyToOneRel, ManyToManyField, ManyToManyRel, OneToOneField, OneToOneRel

from django_object.datatypes import PaginatedList
from django_object.utils import extract_fields_from_model, determine_items
from object.datatypes import IntegerType, StringType, BooleanType, FloatType, DateType, TimeType, DateTimeType, \
    ObjectType


@singledispatch
def convert_django_field(field, field_name, both_fields, input_fields, output_fields):
    raise NotImplementedError(field.__class__)


@convert_django_field.register(AutoField)
@convert_django_field.register(IntegerField)
def convert_to_integer_type(field, field_name, both_fields, input_fields, output_fields):
    both_fields[field_name] = IntegerType(nullable=field.null)


@convert_django_field.register(CharField)
@convert_django_field.register(TextField)
def convert_to_string_type(field, field_name, both_fields, input_fields, output_fields):
    both_fields[field_name] = StringType(nullable=field.null)


@convert_django_field.register(BooleanField)
def convert_to_boolean_type(field, field_name, both_fields, input_fields, output_fields):
    both_fields[field_name] = BooleanType(nullable=field.null)


@convert_django_field.register(FloatField)
def convert_to_float_type(field, field_name, both_fields, input_fields, output_fields):
    both_fields[field_name] = FloatType(nullable=field.null)


@convert_django_field.register(DateField)
def convert_to_date_type(field, field_name, both_fields, input_fields, output_fields):
    both_fields[field_name] = DateType(nullable=field.null)


@convert_django_field.register(TimeField)
def convert_to_time_type(field, field_name, both_fields, input_fields, output_fields):
    both_fields[field_name] = TimeType(nullable=field.null)


@convert_django_field.register(DateTimeField)
def convert_to_date_time_type(field, field_name, both_fields, input_fields, output_fields):
    both_fields[field_name] = DateTimeType(nullable=field.null)


@convert_django_field.register(ForeignKey)
@convert_django_field.register(OneToOneField)
def convert_to_object_type(field, field_name, both_fields, input_fields, output_fields):
    target_model = field.remote_field.model
    input_fields[field_name + "_id"] = IntegerType(nullable=field.null)
    output_fields[field_name] = ObjectType(target_model, nullable=field.null)


@convert_django_field.register(OneToOneRel)
def convert_to_readonly_object_type(field, field_name, both_fields, input_fields, output_fields):
    target_model = field.remote_field.model
    # for OneToOneRel, we don't want to generate filters, as one_to_one_rel_id does not exist in Django
    output_fields[field_name] = ObjectType(target_model, nullable=field.null, only_filters=())


@convert_django_field.register(ManyToOneRel)
@convert_django_field.register(ManyToManyField)
@convert_django_field.register(ManyToManyRel)
def convert_to_readonly_list_of_object_type(field, field_name, both_fields, input_fields, output_fields):
    target_model = field.remote_field.model
    output_fields[field_name] = PaginatedList(target_model)


def get_all_simple_api_model_fields(fields):
    both_fields = OrderedDict()
    input_fields = OrderedDict()
    output_fields = OrderedDict()
    for field_name, field in fields.items():
        convert_django_field(field, field_name, both_fields, input_fields, output_fields)
    return both_fields, input_fields, output_fields


def determine_simple_api_fields(model,
                                only_fields=None, exclude_fields=None, custom_fields=None,
                                input_only_fields=None, input_exclude_fields=None, input_custom_fields=None,
                                output_only_fields=None, output_exclude_fields=None, output_custom_fields=None,
                                ):
    all_model_fields = extract_fields_from_model(model)
    all_fields, all_input_fields, all_output_fields = get_all_simple_api_model_fields(all_model_fields)

    fields = determine_items(all_fields, only_fields, exclude_fields, custom_fields)
    input_fields = determine_items(all_input_fields, input_only_fields, input_exclude_fields, input_custom_fields)
    output_fields = determine_items(all_output_fields, output_only_fields, output_exclude_fields, output_custom_fields)
    return fields, input_fields, output_fields
