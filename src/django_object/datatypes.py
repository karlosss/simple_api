from object.datatypes import ObjectType, PlainListType, IntegerType
from object.object import Object, ObjectMeta
from object.registry import object_storage
from utils import AttrDict

DEFAULT_LIMIT = 20


def resolve_filtering(request, parent_val, params, **kwargs):
    ordering = params.pop("ordering", ())
    qs = parent_val.filter(**params).order_by(*ordering)
    return AttrDict(count=qs.count(), data=qs)


class PaginatedList(ObjectType):
    def __init__(self, to, nullable=False, default=None,
                 nullable_if_input=None, default_if_input=None, **kwargs):
        super().__init__(to=to, nullable=nullable, default=default, resolver=resolve_filtering,
                         nullable_if_input=nullable_if_input, default_if_input=default_if_input, **kwargs)

    def convert(self, adapter, **kwargs):
        self.set_ref()
        object_name = self.to.__name__
        object_module = self.to.__module__

        cls = object_storage.get(object_module, object_name)
        self.parameters = cls.filters

        list_cls = object_storage.get(object_module, object_name + "List")
        obj = ObjectType(list_cls, parameters=self.parameters)
        obj.resolver = self.resolver
        return obj.convert(adapter, **kwargs)

    def to_string(self):
        return "Paginated[{}]".format(self.to.__name__)


def create_associated_list_type(cls):
    def resolve_pagination(request, parent_val, params, **kwargs):
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
                resolver=resolve_pagination
            )
        }
    }
    ObjectMeta(cls.__name__ + "List", (Object,), attrs, module=cls.__module__)
