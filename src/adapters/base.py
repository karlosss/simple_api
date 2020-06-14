class Adapter:
    def __init__(self, objects, extra_actions=None):
        self.objects = objects
        self.extra_actions = extra_actions or {}

    def check(self):
        # check for duplicate class names
        names = set()
        for obj in self.objects:
            assert obj.__name__ not in names, "Duplicate object name: `{}`".format(obj.__name__)
            names.add(obj.__name__)

    def convert_field(self, field, **kwargs):  # called in double dispatch from field
        raise NotImplementedError

    def convert_action(self, action, **kwargs):  # called in double dispatch from action
        raise NotImplementedError

    def convert_function(self, function, **kwargs):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError

    def generate_api(self):
        self.check()
        return self.generate()
