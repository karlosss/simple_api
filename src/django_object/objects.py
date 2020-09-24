from object.datatypes import IntegerType, PlainListType, ObjectType, StringType
from object.function import Function
from object.object import Object, ObjectMeta
from utils import AttrDict

DEFAULT_LIMIT = 20
# todo max limit?


def create_list(of_type, object_name, filters=None, default_limit=DEFAULT_LIMIT):
    def resolve_pagination(request, parent_val, params):
        return parent_val[params["offset"]:(params["offset"] + params["limit"])]

    def resolve_filtering(request, parent_val, params):
        ordering = params.pop("ordering", None)
        qs = parent_val.filter(**params).order_by(*ordering)
        return AttrDict(count=qs.count(), data=qs)

    attrs = {
        "fields": {
            "count": IntegerType(),
            "data": PlainListType(
                of_type,
                parameters={
                    "limit": IntegerType(nullable=True, default=default_limit),
                    "offset": IntegerType(nullable=True, default=0),
                },
                resolver=Function(resolve_pagination)
            )
        }
    }
    return ObjectType(ObjectMeta("{}List".format(object_name), (Object,), attrs),
                      parameters={**filters, "ordering": PlainListType(StringType(), nullable=True)},
                      resolver=Function(resolve_filtering))
