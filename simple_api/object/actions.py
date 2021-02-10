from simple_api.object.function import TemplateFunction
from simple_api.object.permissions import build_permissions_fn
from simple_api.object.validators import build_validation_fn


class ToActionMixin:
    def to_action(self):
        raise NotImplementedError


class SetReferencesMixin:
    def __init__(self, **kwargs):
        self.parent_class = None
        self.name = None
        super().__init__(**kwargs)

    def set_name(self, name):
        self.name = name

    def set_parent_class(self, cls):
        self.parent_class = cls
        for field in {**self.parameters, **self.data}.values():
            field.set_parent_class(cls)
        if self.return_value is not None:
            self.return_value.set_parent_class(cls)


class Action(SetReferencesMixin, ToActionMixin):
    def __init__(self, parameters=None, data=None, return_value=None, exec_fn=None, permissions=None, validators=None,
                 **kwargs):
        self.parameters = parameters or {}
        self.data = data or {}
        self.return_value = return_value
        self.exec_fn = exec_fn
        self.permissions = permissions or ()
        self.validators = validators or ()
        self.kwargs = kwargs
        self._fn = None

        self.hidden = kwargs.get("hidden", False)
        self.with_object = kwargs.get("with_object", False)
        self.hide_if_denied = kwargs.get("hide_if_denied", False)
        self.retry_in = kwargs.get("retry_in")

        for name, param in {**self.parameters, **self.data}.items():
            assert param.nullable or param.default is None, \
                "Cannot set a default value for a non-null parameter `{}`.".format(name)

        super().__init__()

    def get_fn(self):
        if self._fn is None:
            self._fn = TemplateFunction(self.exec_fn)
            self._fn.set_validation_hook(build_validation_fn(self.validators))
            self._fn.set_permissions_hook(build_permissions_fn(self.permissions))
        return self._fn

    def get_return_value(self):
        return self.return_value

    def has_permission(self, *args, **kwargs):
        return build_permissions_fn(self.permissions)(*args, **kwargs)

    def is_valid(self, *args, **kwargs):
        return build_validation_fn(self.validators)(*args, **kwargs)

    def convert(self, adapter, **kwargs):
        return adapter.convert_action(self, **kwargs)

    def to_action(self):
        return self
