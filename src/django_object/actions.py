from object.actions import Action


class DetailAction(Action):
    def __init__(self, only_fields=None, exclude_fields=None, extra_fields=None,
                 return_value=None, exec_fn=None, **kwargs):
        if parameters is None:
            parameters = {}
        self.parameters = parameters
        self.return_value = return_value
        self.exec_fn = exec_fn
        self.parent_class = None
        self.kwargs = kwargs
