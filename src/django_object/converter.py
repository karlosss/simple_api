from collections import OrderedDict
from functools import singledispatch

from django.db.models import AutoField, IntegerField, CharField, TextField, BooleanField, FloatField, DateField, \
    TimeField, DateTimeField, ForeignKey, ManyToOneRel, ManyToManyField, ManyToManyRel, OneToOneField, OneToOneRel, \
    NOT_PROVIDED

from django_object.datatypes import PaginatedList
from django_object.utils import extract_fields_from_model, determine_items, get_pk_field
from django_object.validators import FieldValidator
from object.datatypes import IntegerType, StringType, BooleanType, FloatType, DateType, TimeType, DateTimeType, \
    ObjectType

DJANGO_SIMPLE_API_MAP = {
    AutoField: IntegerType,
    IntegerField: IntegerType,
    CharField: StringType,
    TextField: StringType,
    BooleanField: BooleanType,
    FloatField: FloatType,
    DateField: DateType,
    TimeField: TimeType,
    DateTimeField: DateTimeType,
}


def get_default(field):
    if field.default == NOT_PROVIDED:
        return None
    return field.default


@singledispatch
def convert_django_field(field, field_name, both_fields, input_fields, output_fields, field_validators):
    raise NotImplementedError(field.__class__)


@convert_django_field.register(AutoField)
@convert_django_field.register(IntegerField)
@convert_django_field.register(CharField)
@convert_django_field.register(TextField)
@convert_django_field.register(BooleanField)
@convert_django_field.register(FloatField)
@convert_django_field.register(DateField)
@convert_django_field.register(TimeField)
@convert_django_field.register(DateTimeField)
def convert_to_primitive_type(field, field_name, both_fields, input_fields, output_fields, field_validators):
    assert field.__class__ in DJANGO_SIMPLE_API_MAP, "Cannot convert `{}`".format(field.__class__)
    both_fields[field_name] = DJANGO_SIMPLE_API_MAP[field.__class__](nullable=field.null,
                                                                     default=get_default(field), exclude_filters=())


@convert_django_field.register(ForeignKey)
@convert_django_field.register(OneToOneField)
def convert_to_object_type(field, field_name, both_fields, input_fields, output_fields, field_validators):
    target_model = field.remote_field.model
    pk_field_name, pk_field = get_pk_field(target_model)
    converted_pk_field = DJANGO_SIMPLE_API_MAP[pk_field.__class__]

    input_fields[field_name + "_id"] = converted_pk_field(nullable=field.null, exclude_filters=())
    output_fields[field_name] = ObjectType(target_model, nullable=field.null, exclude_filters=())
    field_validators[field_name + "_id"] = FieldValidator(fn=lambda: target_model.objects.all(),
                                                          type=PaginatedList(target_model),
                                                          field=get_pk_field(target_model)[0])


@convert_django_field.register(OneToOneRel)
def convert_to_readonly_object_type(field, field_name, both_fields, input_fields, output_fields, field_validators):
    target_model = field.remote_field.model
    # for OneToOneRel, we don't want to generate filters, as one_to_one_rel_id does not exist in Django
    output_fields[field_name] = ObjectType(target_model, nullable=field.null)


@convert_django_field.register(ManyToOneRel)
@convert_django_field.register(ManyToManyField)
@convert_django_field.register(ManyToManyRel)
def convert_to_readonly_list_of_object_type(field, field_name, both_fields, input_fields, output_fields,
                                            field_validators):
    target_model = field.remote_field.model
    output_fields[field_name] = PaginatedList(target_model)


def get_all_simple_api_model_fields(fields):
    both_fields = OrderedDict()
    input_fields = OrderedDict()
    output_fields = OrderedDict()
    field_validators = {}

    for field_name, field in fields.items():
        convert_django_field(field, field_name, both_fields, input_fields, output_fields, field_validators)
    return both_fields, input_fields, output_fields, field_validators


def determine_simple_api_fields(model, only_fields=None, exclude_fields=None,
                                custom_fields=None, input_custom_fields=None, output_custom_fields=None):
    all_model_fields = extract_fields_from_model(model)
    filtered_field_names = determine_items(set(all_model_fields.keys()), only_fields, exclude_fields, None)

    filtered_model_fields = OrderedDict()
    for k, v in all_model_fields.items():
        if k in filtered_field_names:
            filtered_model_fields[k] = v

    fields, input_fields, output_fields, validators = get_all_simple_api_model_fields(filtered_model_fields)
    output_fields["__str__"] = StringType(resolver=lambda **kw: kw["obj"].__str__())

    fields.update(custom_fields or {})
    input_fields.update(input_custom_fields or {})
    output_fields.update(output_custom_fields or {})
    return fields, input_fields, output_fields, validators
