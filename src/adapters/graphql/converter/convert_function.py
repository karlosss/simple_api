def convert_function_as_field_resolver(function):
    def resolver(root, info, **kwargs):
        # this getattr is why we need auto_camelcase=False, due to Django
        ret = function.callable(info.context, getattr(root, info.field_name), kwargs)
        return ret
    return resolver


def convert_function_as_exec_fn(function):
    def exec_fn(root, info, **kwargs):
        ret = function.callable(info.context, kwargs)
        return ret
    return exec_fn
