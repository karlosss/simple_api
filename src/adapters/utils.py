from object.registry import object_storage


class TemplateGenerator:
    generate_pre_hook = None


def generate(adapter, extra_actions=None):
    if TemplateGenerator.generate_pre_hook is not None:
        TemplateGenerator.generate_pre_hook()

    if extra_actions:
        for action_name, action in extra_actions.items():
            action.set_name(action_name)
    return adapter(tuple(object_storage.storage.values()), extra_actions).generate_api()
