from object.function import TemplateFunction


class Action:
    def __init__(self, parameters=None, data=None, return_value=None, exec_fn=None, **kwargs):
        self.parameters = parameters or {}
        self.data = data or {}
        self.return_value = return_value
        self.fn = TemplateFunction(exec_fn)
        self.parent_class = None
        self.name = None
        self.kwargs = kwargs

        for name, param in {**self.parameters, **self.data}.items():
            assert param.nullable or param.default is None, \
                "Cannot set a default value for a non-null parameter `{}`.".format(name)

    def set_name(self, name):
        self.name = name

    def set_parent_class(self, cls):
        self.parent_class = cls
        for field in {**self.parameters, **self.data}.values():
            field.set_parent_class(cls)
        if self.return_value is not None:
            self.return_value.set_parent_class(cls)

    def get_fn(self):
        return self.fn

    def get_return_value(self):
        return self.return_value

    def convert(self, adapter, **kwargs):
        return adapter.convert_action(self, **kwargs)
