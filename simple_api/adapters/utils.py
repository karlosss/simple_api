from simple_api.object.registry import object_storage
from simple_api.object.meta_types import build_object_info, build_action_info, build_type_info


class TemplateGenerator:
    generate_pre_hook = None  # place for a hook to create Objects for missing Django models


def generate(adapter, extra_actions=None):
    extra_actions = extra_actions or {}

    if TemplateGenerator.generate_pre_hook is not None:
        TemplateGenerator.generate_pre_hook()

    for action_name, action in extra_actions.items():
        action.set_name(action_name)

    object_info = build_object_info()
    type_info = build_type_info()
    action_info = build_action_info(extra_actions)
    extra_actions["__types"] = type_info
    extra_actions["__objects"] = object_info
    extra_actions["__actions"] = action_info

    return adapter(tuple(object_storage.storage.values()), extra_actions).generate_api()
