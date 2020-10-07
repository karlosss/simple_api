class Function:
    def __init__(self, callable):
        self.callable = callable

    def convert(self, adapter, **kwargs):
        return adapter.convert_function(self, **kwargs)


class TemplateFunction:
    def __init__(self, main_hook):
        self.default_hook = lambda *args, **kwargs: None
        self.pre_hook = lambda *args, **kwargs: None
        self.main_hook = main_hook
        self.pre_hook_set = False
        self.default_hook_set = False

    def set_pre_hook(self, hook):
        if hook is not None:
            self.pre_hook = hook
            self.pre_hook_set = True
        return self

    def set_main_hook(self, hook):
        self.main_hook = hook
        return self

    def set_default_hook(self, hook):
        if hook is not None:
            self.default_hook = hook
            self.default_hook_set = True
        return self

    def convert(self, adapter, **kwargs):
        def callable(*args, **kwargs):
            self.pre_hook(*args, **kwargs)
            result = self.main_hook(*args, **kwargs)
            if result is None:
                return self.default_hook(*args, **kwargs)
            return result

        f = Function(callable)
        return adapter.convert_function(f, **kwargs)
