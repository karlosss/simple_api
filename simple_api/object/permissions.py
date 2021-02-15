from inspect import isclass


# instantiates permission classes (if they are not already, maybe due to get_fn injection) and builds a
# function that raises if the permissions are not passed
def build_permissions_fn(permissions):
    instantiated_permissions = []
    for cls_or_inst in permissions:
        if isclass(cls_or_inst) or isinstance(cls_or_inst, LogicalConnector):
            instantiated_permissions.append(cls_or_inst())
        else:
            instantiated_permissions.append(cls_or_inst)

    def fn(**kwargs):
        for perm in instantiated_permissions:
            if not perm.has_permission(**kwargs):
                raise PermissionError(perm.error_message(**kwargs))
    return fn


class BasePermission:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def permission_statement(self, **kwargs):
        raise NotImplementedError

    def has_permission(self, exclude_classes=(), **kwargs):
        for cls in reversed(self.__class__.__mro__):
            if cls in (object, BasePermission, LogicalResolver) + exclude_classes:
                continue
            if not cls.permission_statement(self, **kwargs):
                return False
        return True

    def error_message(self, **kwargs):
        return "You do not have permission to access this."


class LogicalConnector:
    def __init__(self, *permissions):
        self.permissions = permissions

    def __call__(self, **kwargs):
        instantiated_perms = []
        for perm in self.permissions:
            assert isclass(perm) or isinstance(perm, LogicalConnector), \
                "Permissions in logical connectors must be classes."
            instantiated_perms.append(perm(**kwargs))
        return LogicalResolver(instantiated_perms, self.resolve_fn)

    def resolve_fn(self, permissions, **kwargs):
        raise NotImplementedError


class LogicalResolver:
    def __init__(self, permissions, resolve_fn):
        self.permissions = permissions
        self.resolve_fn = resolve_fn

    def has_permission(self, **kwargs):
        return self.resolve_fn(self.permissions, **kwargs)

    def error_message(self, **kwargs):
        return "You do not have permission to access this."


class Or(LogicalConnector):
    def resolve_fn(self, permissions, **kwargs):
        for perm in permissions:
            if perm.has_permission(**kwargs):
                return True
        return False


class And(LogicalConnector):
    def resolve_fn(self, permissions, **kwargs):
        for perm in permissions:
            if not perm.has_permission(**kwargs):
                return False
        return True


class Not(LogicalConnector):
    def resolve_fn(self, permissions, **kwargs):
        assert len(permissions) == 1, "`Not` accepts only one permission class as parameter."
        return not permissions[0].has_permission(**kwargs)


class AllowAll(BasePermission):
    def permission_statement(self, **kwargs):
        return True


class AllowNone(BasePermission):
    def permission_statement(self, **kwargs):
        return False
