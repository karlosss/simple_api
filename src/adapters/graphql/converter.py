from functools import singledispatch

import graphene

from adapters.graphql.registry import get_class
from adapters.graphql.utils import in_kwargs_and_true, pop_if_present
from object.fields import StringField, IntegerField, ObjectField


def convert_field(field, **kwargs):
    if in_kwargs_and_true("input", kwargs):
        cls = graphene.Argument
    else:
        cls = graphene.Field
    pop_if_present("input", kwargs)
    return convert_field_as(field, cls, **kwargs)


@singledispatch
def convert_field_as(field, cls, **kwargs):
    raise NotImplementedError


@convert_field_as.register(StringField)
def convert_field_as_string(field, cls, **kwargs):
    return cls(graphene.String, required=not field.nullable, default_value=field.default, **kwargs)


@convert_field_as.register(IntegerField)
def convert_field_as_string(field, cls, **kwargs):
    return cls(graphene.Int, required=not field.nullable, default_value=field.default, **kwargs)


@convert_field_as.register(ObjectField)
def convert_field_as_object(field, cls, **kwargs):

    # differentiate between Argument and Field (ObjectType vs. InputObjectType)
    if cls == graphene.Argument:
        to = get_class(field.to).input
    else:
        to = get_class(field.to).output

    return cls(to, required=not field.nullable, default_value=field.default, **kwargs)
