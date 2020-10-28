from object.actions import Action
from object.meta_resolvers import object_info
from object.object import Object
from object.datatypes import PlainListType, ObjectType, DurationType, StringType, BooleanType


class ChoiceInfo(Object):
    fields = {
        "parameter_name": StringType(),
        "action_name": StringType(),
        "field_name": StringType()
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


def build_object_info():
    return Action(return_value=PlainListType(ObjectType(ObjectInfo)),
                  exec_fn=object_info)
