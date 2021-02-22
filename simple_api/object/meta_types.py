from simple_api.object.actions import Action
from simple_api.object.meta_resolvers import object_info, build_action_info_fn
from simple_api.object.object import Object
from simple_api.object.datatypes import PlainListType, ObjectType, DurationType, StringType, BooleanType


class TypeInfo(Object):
    fields = {
        "typename": StringType(),
        "nullable": BooleanType(),
        # TODO default value
    }
    hidden = True


class InputFieldInfo(Object):
    fields = {
        "name": StringType(),
        "type": ObjectType(TypeInfo),
    }
    hidden = True


class ActionInfo(Object):
    fields = {
        "name": StringType(),
        "parameters": PlainListType(ObjectType(InputFieldInfo)),
        "data": PlainListType(ObjectType(InputFieldInfo)),
        "return_type": ObjectType(TypeInfo),

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
