from collections import OrderedDict

from object.datatypes import PlainListType, IntegerType, ObjectType, StringType
from object.function import Function
from object.object import ObjectMeta, Object
from object.registry import object_storage
from utils import AttrDict


DEFAULT_LIMIT = 20


object_type_paginated_list = {}


def build_parameters_for_paginated_list(filters=None):
    if filters is None:
        filters = {}
    return {**filters, "ordering": PlainListType(StringType(), nullable=True)}


def resolve_filtering(request, parent_val, params):
    ordering = params.pop("ordering", None)
    qs = parent_val.filter(**params).order_by(*ordering)
    return AttrDict(count=qs.count(), data=qs)


def paginated_list(inner_type, object_module, object_name, filters=None, default_limit=DEFAULT_LIMIT):
    def resolve_pagination(request, parent_val, params):
        return parent_val[params["offset"]:(params["offset"] + params["limit"])]

    if not object_storage.class_exists(object_module, object_name):
        attrs = {
            "fields": OrderedDict({
                "count": IntegerType(),
                "data": PlainListType(
                    ObjectType(inner_type),
                    parameters={
                        "limit": IntegerType(nullable=True, default=default_limit),
                        "offset": IntegerType(nullable=True, default=0),
                    },
                    resolver=Function(resolve_pagination)
                )
            })
        }
        cls = ObjectMeta(object_name, (Object,), attrs, module=object_module)
        object_storage.store(object_module, object_name, cls)
    else:
        cls = object_storage.get(object_module, object_name)

    obj = ObjectType(cls,
                     parameters=build_parameters_for_paginated_list(filters),
                     resolver=Function(resolve_filtering))
    return obj
