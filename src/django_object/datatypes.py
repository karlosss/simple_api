from object.datatypes import ObjectType, PlainListType, StringType, IntegerType
from object.function import Function
from object.object import Object, ObjectMeta
from object.registry import object_storage
from utils import AttrDict

DEFAULT_LIMIT = 20


def build_parameters_for_paginated_list(filters=None):
    if filters is None:
        filters = {}
    filters.update({"ordering": PlainListType(StringType(), nullable=True)})
    return filters


def resolve_filtering(request, parent_val, params):
    ordering = params.pop("ordering", None)
    qs = parent_val.filter(**params).order_by(*ordering)
    return AttrDict(count=qs.count(), data=qs)


class PaginatedList(ObjectType):
    def __init__(self, to, filters=None, nullable=False, default=None,
                 nullable_if_input=None, default_if_input=None):
        if filters is None:
            filters = {}
        super().__init__(to=to, nullable=nullable, default=default,
                         parameters=build_parameters_for_paginated_list(filters), resolver=Function(resolve_filtering),
                         nullable_if_input=nullable_if_input, default_if_input=default_if_input)

    def convert(self, adapter, **kwargs):
        self.set_ref()
        object_name = self.to.__name__ + "List"
        object_module = self.to.__module__
        cls = object_storage.get(object_module, object_name)
        obj = ObjectType(cls, parameters=self.parameters, resolver=self.resolver)
        return obj.convert(adapter, **kwargs)

    def to_string(self):
        return "Paginated[{}]".format(self.to.__name__)


def create_associated_list_type(cls):
    def resolve_pagination(request, parent_val, params):
        return parent_val[params["offset"]:(params["offset"] + params["limit"])]

    attrs = {
        "fields": {
            "count": IntegerType(),
            "data": PlainListType(
                ObjectType(cls),
                parameters={
                    "limit": IntegerType(nullable=True, default=20),
                    "offset": IntegerType(nullable=True, default=0),
                },
                resolver=Function(resolve_pagination)
            )
        }
    }
    ObjectMeta(cls.__name__ + "List", (Object,), attrs, module=cls.__module__)
