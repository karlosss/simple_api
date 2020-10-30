from copy import deepcopy

from object.function import TemplateFunction
from object.permissions import permissions_pre_hook


class Action:
    def __init__(self, parameters=None, return_value=None, exec_fn=None, permissions=None, validator=None,
                 field_validators=None, **kwargs):
        self.parameters = parameters or {}
        self.return_value = deepcopy(return_value)
        self.permissions = None
        self.validator = None
        self.field_validators = field_validators or {}
        self.has_permission = None
        self.fn = TemplateFunction(exec_fn)
        self.parent_class = None
        self.name = None
        self.kwargs = kwargs
        self.retry_in = kwargs.get("retry_in")
        self.hide_if_denied = kwargs.get("hide_if_denied", False)
        self.hidden = kwargs.get("hidden", False)

        self.set_permissions(permissions)
        self.set_validator(validator)

        for name, param in self.parameters.items():
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

    def get_fn(self):
        return self.fn

    def get_return_value(self):
        return self.return_value

    def set_permissions(self, permission_classes):
        self.permissions = permission_classes
        self.has_permission = permissions_pre_hook(permission_classes)
        self.fn.set_pre_hook(self.has_permission)

    def set_validator(self, validator):
        self.fn.set_validate_hook(validator)
        self.validator = validator

    def convert(self, adapter, **kwargs):
        return adapter.convert_action(self, **kwargs)
