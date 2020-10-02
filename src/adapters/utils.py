from object.registry import object_storage


def generate(adapter, extra_actions=None):
    if extra_actions:
        for action_name, action in extra_actions.items():
            action.set_name(action_name)
    return adapter(tuple(object_storage.storage.values()), extra_actions).generate_api()
