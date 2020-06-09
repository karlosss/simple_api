class Action:
    def __init__(self, parameters=None, return_value=None, exec_fn=None):
        if parameters is None:
            parameters = {}
        self.parameters = parameters
        self.return_value = return_value
        self.exec_fn = exec_fn
        self.parent_class = None

    def set_parent_class(self, cls):
        self.parent_class = cls
        for field in self.parameters.values():
            field.set_parent_class(cls)
        self.return_value.set_parent_class(cls)

    def convert(self, adapter, **kwargs):
        return adapter.convert_action(self, **kwargs)
