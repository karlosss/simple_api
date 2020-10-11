from copy import deepcopy

from object.datatypes import PlainListType, ObjectType, DurationType, StringType, BooleanType
from object.object import ObjectMeta, Object
from object.registry import object_storage


def build_action_type(obj):
    return PlainListType(ObjectType(obj), parameters={"name": StringType(nullable=True)})


def build_action_type_fields():
    return {
        "fields": {
            "name": StringType(),
            "permitted": BooleanType(),
            "deny_reason": StringType(nullable=True),
            "retry_in": DurationType(nullable=True),
        }
    }


def build_action_type_resolver(actions, in_object=None):
    def resolver(**kwargs):
        filter_name = kwargs["params"].get("name")
        out = []
        for name, action in actions.items():
            if action.list_in_object and in_object is False:
                continue
            elif not action.list_in_object and in_object is True:
                continue

            if filter_name and name != filter_name:
                continue
            try:
                action.has_permission(**kwargs)
                permitted = True
            except PermissionError as e:
                if action.hide_if_denied:
                    continue
                permitted = False
                deny_reason = str(e)

            action_data = {
                "name": name,
                "permitted": permitted,
                "deny_reason": deny_reason if not permitted else None,
                "retry_in": action.retry_interval
            }
            out.append(action_data)
        return out
    return resolver


def build_actions_field():
    def _filter_actions(**kwargs):
        name = kwargs["params"].get("name")
        out = []
        for action in kwargs["parent_val"]:
            if name and action["name"] != name:
                continue
            out.append(action)
        return out

    field = deepcopy(ObjectMeta.get_action_type())
    field.resolver.set_main_hook(_filter_actions)
    return field


class Type(Object):
    fields = {
        "name": StringType(),
        "__actions": build_actions_field()
    }


def build_types_field():
    return PlainListType(ObjectType(Type))


def get_types_actions(**kwargs):
    name = kwargs["params"].get("name")
    out = []
    for cls in object_storage.storage.values():
        if name and cls.__name__ != name:
            continue
        if cls.actions:
            out.append({
                "name": cls.__name__,
                "__actions": build_action_type_resolver(cls.actions, in_object=False)(params={})
            })
    return out
