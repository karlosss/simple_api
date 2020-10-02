from collections import OrderedDict

from django.db.models import ManyToOneRel, ManyToManyRel, OneToOneRel


def extract_fields_from_model(model):
    fields = OrderedDict()

    for field in model._meta.fields:
        fields[field.name] = field

    for field in model._meta.local_many_to_many:
        if field.name not in fields:
            fields[field.name] = field

    for name, attr in model.__dict__.items():
        # Don't overwrite any already extracted fields
        if name in fields:
            continue

        related = getattr(attr, "rel", getattr(attr, "related", None))
        if isinstance(related, (ManyToOneRel, ManyToManyRel, OneToOneRel)):
            fields[name] = related

    return fields


def all_field_names(model):
    return tuple(extract_fields_from_model(model).keys())


def determine_fields(model, only_fields, exclude_fields):
    assert only_fields is None or exclude_fields is None, "Cannot define both `only_fields` and `exclude_fields.`"

    all_fields = all_field_names(model)

    if only_fields is None and exclude_fields is None:
        exclude_fields = ()

    if only_fields is not None:
        fields = []
        if not isinstance(only_fields, (list, tuple)):
            only_fields = only_fields,
        for field in only_fields:
            assert field in all_fields, "Unknown field: `{}`.".format(field)
            fields.append(field)
        return tuple(fields)

    if not isinstance(exclude_fields, (list, tuple)):
        exclude_fields = exclude_fields,

    for field in exclude_fields:
        assert field in all_fields, "Unknown field: {}.".format(field)

    return tuple(f for f in all_fields if f not in exclude_fields)


def filter_fields_from_model(model, only_fields, exclude_fields):
    all_fields = extract_fields_from_model(model)
    field_names = determine_fields(model, only_fields, exclude_fields)

    fields = OrderedDict()

    for field in all_fields:
        if field in field_names:
            fields[field] = all_fields[field]

    return fields
