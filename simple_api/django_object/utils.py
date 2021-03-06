from collections import OrderedDict
from copy import deepcopy

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


def _handle_item(item, t1, t2, all_on_none):
    if t1 is None and t2 is None:
        if all_on_none:
            return t1, t2
        else:
            return (item,), None
    if t1 is None:
        return None, tuple(f for f in t2 if f != item)
    if item not in t1:
        t1 = t1 + (item,)
    return t1, None


def add_item(item, only, exclude, all_on_none=True):
    return _handle_item(item, only, exclude, all_on_none)


def remove_item(item, only, exclude, all_on_none=True):
    return _handle_item(item, exclude, only, not all_on_none)[::-1]


def determine_items(all, only, exclude, custom, fail_on_nonexistent=True, in_place=False, all_on_none=True):
    assert only is None or exclude is None, "Cannot define both `only` and `exclude` on item filtering."

    if not in_place:
        all = deepcopy(all)

    if custom is None:
        custom = {}

    if only is None and exclude is None:
        if all_on_none:
            exclude = ()
        else:
            only = ()

    if only is not None and not isinstance(only, (list, tuple)):
        only = only,
    if exclude is not None and not isinstance(exclude, (list, tuple)):
        exclude = exclude,

    if fail_on_nonexistent:
        if only is not None:
            for item in only:
                if item not in all:
                    raise KeyError(item)
        if exclude is not None:
            for item in exclude:
                if item not in all:
                    raise KeyError(item)

    if only is not None:
        if isinstance(all, set):
            to_remove = all.difference(set(only))
        else:
            to_remove = set(all.keys()).difference(set(only))

        for f in to_remove:
            if isinstance(all, set):
                all.remove(f)
            else:
                del all[f]
    else:
        for f in exclude:
            if isinstance(all, set):
                all.remove(f)
            else:
                del all[f]

    all.update(custom)
    return all


def determine_model_fields(model, only_fields, exclude_fields):
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
    field_names = determine_model_fields(model, only_fields, exclude_fields)

    fields = OrderedDict()

    for field in all_fields:
        if field in field_names:
            fields[field] = all_fields[field]

    return fields


def get_pk_field(model):
    return model._meta.pk.name, model._meta.pk
