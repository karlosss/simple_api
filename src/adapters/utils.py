def generate(adapter, objs, extra_actions=None):
    return adapter(objs, extra_actions).generate_api()
