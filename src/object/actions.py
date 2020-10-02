class Action:
    def __init__(self, parameters=None, return_value=None, exec_fn=None, **kwargs):
        if parameters is None:
            parameters = {}
        self.parameters = parameters
        self.return_value = return_value
        self.exec_fn = exec_fn
        self.parent_class = None
        self.name = None
        self.kwargs = kwargs

        for name, param in parameters.items():
            assert param.nullable or param.default is None, \
                "Cannot set a default value for a non-null parameter `{}`.".format(name)

    def set_name(self, name):
        self.name = name

    def set_parent_class(self, cls):
        self.parent_class = cls
        for field in self.parameters.values():
            field.set_parent_class(cls)
        if self.return_value is not None:
            self.return_value.set_parent_class(cls)

    def get_exec_fn(self):
        return self.exec_fn

    def get_return_value(self):
        return self.return_value

    def convert(self, adapter, **kwargs):
        return adapter.convert_action(self, **kwargs)
