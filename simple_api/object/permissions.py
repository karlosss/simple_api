from inspect import isclass


def build_permissions_fn(permissions):
    def fn(**kwargs):
        for perm in permissions:
            if not perm().has_permission(**kwargs):
                raise PermissionError(perm().error_message(**kwargs))
    return fn


class BasePermission:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def permission_statement(self, **kwargs):
        raise NotImplementedError

    def has_permission(self, **kwargs):
        # to achieve hierarchical checking for permissions (a subclass calls the permission statement of the superclass
        # and only if it passes, executes its own), we need to traverse over the whole linearization order of the
        # permission class; however, classes like object, which are naturally also a part of the chain, do not
        # contain the `permission_statement` method and therefore should be just skipped; the same is true for abstract
        # permission classes which contain the method, but is not implemented - like this one for example: to achieve
        # this, we try calling the method and if it turns out to not be implemented, we skip it as well
        for cls in reversed(self.__class__.__mro__):
            if not hasattr(cls, "permission_statement"):
                continue
            try:
                if not cls.permission_statement(self, **kwargs):
                    return False
            except NotImplementedError:
                continue
        return True

    def error_message(self, **kwargs):
        return "You do not have permission to access this."


class LogicalConnector:
    def __init__(self, *permissions):
        self.permissions = permissions

    def __call__(self, **kwargs):
        for perm in self.permissions:
            assert isclass(perm) or isinstance(perm, LogicalConnector), \
                "Permissions in logical connectors must be classes."
        return LogicalResolver(self.permissions, self.resolve_fn)

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
            if perm().has_permission(**kwargs):
                return True
        return False


class And(LogicalConnector):
    def resolve_fn(self, permissions, **kwargs):
        for perm in permissions:
            if not perm().has_permission(**kwargs):
                return False
        return True


class Not(LogicalConnector):
    def resolve_fn(self, permissions, **kwargs):
        assert len(permissions) == 1, "`Not` accepts only one permission class as parameter."
        return not permissions[0]().has_permission(**kwargs)


class AllowAll(BasePermission):
    def permission_statement(self, **kwargs):
        return True


class AllowNone(BasePermission):
    def permission_statement(self, **kwargs):
        return False
