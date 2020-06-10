class Adapter:
    def __init__(self, objects, extra_actions=None):
        self.objects = objects
        self.extra_actions = extra_actions or {}

    def convert_field(self, field, **kwargs):  # called in double dispatch from field
        raise NotImplementedError

    def convert_action(self, action):  # called in double dispatch from action
        raise NotImplementedError

    def convert_function(self, function, **kwargs):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError
