class ClassStub:
    def __init__(self, name=None, bases=None, attrs=None):
        self.name = name
        self.bases = bases or []
        self.attrs = attrs or {}

    def add_base(self, cls):
        self.bases.append(cls)

    def add_attr(self, k, v):
        self.attrs[k] = v

    def build(self, metaclass=type):
        assert self.name is not None, "`name` must be set"
        return metaclass(self.name, tuple(self.bases), self.attrs)


class AttrDict(dict):
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def keys(self):
        return tuple(super().keys())

    def values(self):
        return tuple(super().values())


class StorageMeta(type):
    classes = []

    @classmethod
    def store(mcs, cls):
        mcs.classes.append(cls)

    @classmethod
    def reset(mcs):
        for cls in mcs.classes:
            cls.storage = {}

    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        cls.storage = {}
        return cls


class Storage(metaclass=StorageMeta):
    storage = {}

    def store(self, *args, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError
