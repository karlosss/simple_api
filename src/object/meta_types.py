from object.actions import Action
from object.meta_resolvers import object_info, build_action_info_fn
from object.object import Object
from object.datatypes import PlainListType, ObjectType, DurationType, StringType, BooleanType


class ActionInfo(Object):
    fields = {
        "name": StringType(),
        "permitted": BooleanType(),
        "deny_reason": StringType(nullable=True),
        "retry_in": DurationType(nullable=True),
    }
    hidden = True


class ObjectInfo(Object):
    fields = {
        "name": StringType(),
        "pk_field": StringType(nullable=True),
        "actions": PlainListType(ObjectType(ActionInfo)),
    }
    hidden = True


def build_object_info():
    return Action(return_value=PlainListType(ObjectType(ObjectInfo)),
                  exec_fn=object_info)


def build_action_info(actions):
    return Action(return_value=PlainListType(ObjectType(ActionInfo)),
                  exec_fn=build_action_info_fn(actions))
