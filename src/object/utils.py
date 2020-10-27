from object.actions import Action
from object.object import Object
from object.registry import object_storage
from object.datatypes import PlainListType, ObjectType, DurationType, StringType, BooleanType


class ChoiceInfo(Object):
    fields = {
        "parameter_name": StringType(),
        "action_name": StringType()
    }
    hidden = True


class ActionInfo(Object):
    fields = {
        "name": StringType(),
        "permitted": BooleanType(),
        "deny_reason": StringType(nullable=True),
        "retry_in": DurationType(nullable=True),
        "choices": PlainListType(ObjectType(ChoiceInfo))
    }
    hidden = True


class ObjectInfo(Object):
    fields = {
        "name": StringType(),
        "pk_field": StringType(nullable=True),
        "actions": PlainListType(ObjectType(ActionInfo)),
    }
    hidden = True


def _object_info(**kwargs):
    out = []
    for cls in object_storage.storage.values():
        if getattr(cls, "hidden", False):
            continue
        item = {
            "name": cls.__name__,
            "pk_field": getattr(cls, "pk_field", None),
            "actions": []
        }
        for action in cls.actions.values():
            if getattr(action, "on_object", False):
                continue

            try:
                action.has_permission(request=kwargs["request"])
                permitted = True
                deny_reason = None
            except PermissionError as e:
                if action.hide_if_denied:
                    continue
                permitted = False
                deny_reason = str(e)

            action_item = {
                "name": action.name,
                "permitted": permitted,
                "deny_reason": deny_reason,
                "retry_in": action.retry_in,
                "choices": []
            }
            item["actions"].append(action_item)
        out.append(item)
    return out


def build_object_info():
    return Action(return_value=PlainListType(ObjectType(ObjectInfo)),
                  exec_fn=_object_info)
