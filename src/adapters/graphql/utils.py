def in_kwargs_and_true(param, kwargs):
    return param in kwargs and kwargs[param] is True


def pop_if_present(param, kwargs):
    if param in kwargs:
        kwargs.pop(param)


def decapitalize(s):
    return s[:1].lower() + s[1:] if s else ''
