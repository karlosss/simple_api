from object.datatypes import IntegerType, PlainListType, ObjectType, StringType
from object.function import Function
from object.object import Object, ObjectMeta

DEFAULT_LIMIT = 20


def create_list(of_type, object_name, filters=None, default_limit=DEFAULT_LIMIT):
    def resolve(request, parent_val, params):
        limit = params.pop("limit")
        offset = params.pop("offset")
        ordering = params.pop("ordering", None)

        qs = parent_val.filter(**params)

    attrs = {
        "fields": {
            "count": IntegerType(),
            "data": PlainListType(
                of_type,
                parameters={
                    "limit": IntegerType(nullable=True, default=default_limit),
                    "offset": IntegerType(nullable=True, default=0),
                },
                resolver=Function(resolve)
            )
        }
    }
    return ObjectType(ObjectMeta("{}List".format(object_name), (Object,), attrs), parameters=filters)
