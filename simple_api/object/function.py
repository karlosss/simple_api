class Function:
    def __init__(self, callable):
        self.callable = callable

    def convert(self, adapter, **kwargs):
        return adapter.convert_function(self, **kwargs)


class TemplateFunction:
    def __init__(self, main_hook):
        self.default_hook = lambda *args, **kwargs: None
        self.permissions_hook = lambda *args, **kwargs: None
        self.validation_hook = lambda *args, **kwargs: None
        self.main_hook = main_hook

    def set_permissions_hook(self, hook):
        if hook is not None:
            self.permissions_hook = hook
        return self

    def set_validation_hook(self, hook):
        if hook is not None:
            self.validation_hook = hook
        return self

    def set_default_hook(self, hook):
        if hook is not None:
            self.default_hook = hook
        return self

    def convert(self, adapter, **kwargs):
        def fn(*args, **kwargs):
            self.permissions_hook(*args, **kwargs)
            self.validation_hook(*args, **kwargs)
            result = self.main_hook(*args, **kwargs)
            if result is None:
                return self.default_hook(*args, **kwargs)
            return result

        f = Function(fn)
        return adapter.convert_function(f, **kwargs)
