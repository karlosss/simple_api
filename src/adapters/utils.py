from copy import deepcopy

from object.actions import Action
from object.datatypes import StringType
from object.object import ObjectMeta
from object.permissions import AllowAll
from object.registry import object_storage
from object.utils import build_action_type_resolver


class TemplateGenerator:
    generate_pre_hook = None


def generate(adapter, extra_actions=None):
    extra_actions = extra_actions or {}

    if TemplateGenerator.generate_pre_hook is not None:
        TemplateGenerator.generate_pre_hook()

    if extra_actions:
        for action_name, action in extra_actions.items():
            action.set_name(action_name)
            if not action.permissions:
                action.set_permissions(AllowAll)

    extra_actions["__actions"] = Action(return_value=ObjectMeta.get_action_type(),
                                        parameters={"name": StringType(nullable=True)},
                                        exec_fn=build_action_type_resolver(deepcopy(extra_actions)))
    return adapter(tuple(object_storage.storage.values()), extra_actions).generate_api()
