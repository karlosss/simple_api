class Function:
    def __init__(self, callable):
        self.callable = callable

    def convert(self, adapter, **kwargs):
        return adapter.convert_function(self, **kwargs)
