from object.registry import object_storage


def generate(adapter, extra_actions=None):
    return adapter(tuple(object_storage.storage.values()), extra_actions).generate_api()
