from utils import AttrDict


def convert_function_as_field_resolver(function):
    def resolver(root, info, **kwargs):
        # this getattr is why we need auto_camelcase=False, due to Django
        # in case the attribute is missing, return None instead (this handles Django's missing OneToOneRel)
        if isinstance(root, dict):
            root = AttrDict(**root)
        ret = function.callable(request=info.context, params=kwargs, parent_val=getattr(root, info.field_name, None),
                                obj=root, field_name=info.field_name)
        return ret
    return resolver


def convert_function_as_exec_fn(function):
    def exec_fn(root, info, **kwargs):
        ret = function.callable(request=info.context, params=kwargs, obj=root, field_name=info.field_name)
        return ret
    return exec_fn
