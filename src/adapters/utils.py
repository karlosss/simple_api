from object.permissions import AllowAll
from object.registry import object_storage
from object.meta_types import build_object_info


class TemplateGenerator:
    generate_pre_hook = None  # place for a hook to create Objects for missing Django models


def generate(adapter, extra_actions=None):
    extra_actions = extra_actions or {}

    if TemplateGenerator.generate_pre_hook is not None:
        TemplateGenerator.generate_pre_hook()

    if extra_actions:
        for action_name, action in extra_actions.items():
            action.set_name(action_name)

    return adapter(tuple(object_storage.storage.values()), extra_actions).generate_api()
