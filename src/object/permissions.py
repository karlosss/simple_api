from inspect import isclass


def permissions_pre_hook(permissions):
    if permissions is None:
        return None

    if not isinstance(permissions, (list, tuple)):
        permissions = permissions,

    instantiated_permissions = []
    for cls_or_inst in permissions:
        if isclass(cls_or_inst):
            instantiated_permissions.append(cls_or_inst())
        else:
            instantiated_permissions.append(cls_or_inst)

    def callable(*args, **kwargs):
        for perm in instantiated_permissions:
            if not perm.has_permission(**kwargs):
                raise PermissionError(perm.error_message(**kwargs))
    return callable


class BasePermission:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def permission_statement(self, **kwargs):
        raise NotImplementedError

    def has_permission(self, exclude_classes=(), **kwargs):
        for cls in reversed(self.__class__.__mro__):
            if cls in (object, BasePermission, OrResolver, AndResolver, NotResolver) + exclude_classes:
                continue
            if not cls.permission_statement(self, **kwargs):
                return False
        return True

    def error_message(self, **kwargs):
        return "You do not have permission to access this."


class Or:
    def __init__(self, *permissions):
        self.permissions = permissions

    def __call__(self, **kwargs):
        return OrResolver(self.permissions, **kwargs)


class And:
    def __init__(self, *permissions):
        self.permissions = permissions

    def __call__(self, **kwargs):
        return AndResolver(self.permissions, **kwargs)


class Not:
    def __init__(self, permission_class):
        self.permission_class = permission_class

    def __call__(self, **kwargs):
        return NotResolver(self.permission_class, **kwargs)


class OrResolver(BasePermission):
    def __init__(self, permissions, **kwargs):
        super().__init__(**kwargs)
        self.permissions = permissions

    def has_permission(self, **kwargs):
        for perm in self.permissions:
            if perm.has_permission(**kwargs):
                return True
        return False


class AndResolver(BasePermission):
    def __init__(self, permissions, **kwargs):
        super().__init__(**kwargs)
        self.permissions = permissions

    def has_permission(self, **kwargs):
        for perm in self.permissions:
            if not perm.has_permission(**kwargs):
                return False
        return True


class NotResolver(BasePermission):
    def __init__(self, permission, **kwargs):
        super().__init__(**kwargs)
        self.permission = permission

    def has_permission(self, **kwargs):
        return not self.permission.has_permission(**kwargs)


class AllowAll(BasePermission):
    def permission_statement(self, **kwargs):
        return True


class AllowNone(BasePermission):
    def permission_statement(self, **kwargs):
        return False
