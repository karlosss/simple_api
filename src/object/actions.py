from object.function import TemplateFunction
from object.permissions import permissions_pre_hook


class Action:
    def __init__(self, parameters=None, data=None, return_value=None, exec_fn=None, validators=None, validate_fn=None,
                 permissions=None, **kwargs):
        self.parameters = parameters or {}
        self.data = data or {}
        self.return_value = return_value
        self.exec_fn = exec_fn
        self.parent_class = None
        self.name = None
        self.validators = validators or {}
        self.validate_fn = validate_fn or (lambda *a, **kwa: None)
        self.permissions = permissions or ()
        self.kwargs = kwargs
        self._fn = None

        self.hidden = kwargs.get("hidden", False)
        self.with_object = kwargs.get("with_object", False)
        self.hide_if_denied = kwargs.get("hide_if_denied", False)
        self.retry_in = kwargs.get("retry_in")
        self.choice_map = kwargs.get("choice_map", [])

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
        if self._fn is None:
            self._fn = TemplateFunction(self.exec_fn)
            validators = self.validators

            def validate(*args, **kwargs):
                errors = []
                for field_name, fn in validators.items():
                    # todo move this to to_action so that we don't mix layers
                    if kwargs["params"]["data"][field_name] not in fn(*args, **kwargs).values_list("pk", flat=True):
                        errors.append((field_name, kwargs["params"]["data"][field_name]))
                if errors:
                    s = ""
                    for error in errors:
                        s = s + "`{}` = {}, ".format(*error)
                    s = s[:-2]
                    raise ValueError("Validation failed for {}".format(s))
                self.validate_fn(*args, **kwargs)

            self._fn.set_validate_hook(validate)
            self._fn.set_permissions_hook(permissions_pre_hook(self.permissions))
        return self._fn

    def get_return_value(self):
        return self.return_value

    def has_permission(self, *args, **kwargs):
        return permissions_pre_hook(self.permissions)(*args, **kwargs)

    def convert(self, adapter, **kwargs):
        return adapter.convert_action(self, **kwargs)
