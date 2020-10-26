def permissions_pre_hook(permission_classes):
    if permission_classes is None:
        return None

    if not isinstance(permission_classes, (list, tuple)):
        permission_classes = permission_classes,

    def callable(*args, **kwargs):
        for pc in permission_classes:
            pc_inst = pc(*args, **kwargs)
            if not pc_inst.has_permission():
                raise PermissionError(pc_inst.error_message())
    return callable


class BasePermission:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def permission_statement(self):
        raise NotImplementedError

    def has_permission(self, exclude_classes=()):
        for cls in reversed(self.__class__.__mro__):
            if cls in (object, BasePermission, OrResolver, AndResolver, NotResolver) + exclude_classes:
                continue
            if not cls.permission_statement(self):
                return False
        return True

    def error_message(self):
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
    def __init__(self, permission_classes, **kwargs):
        super().__init__(**kwargs)
        self.permission_classes = permission_classes

    def has_permission(self):
        for permission_class in self.permission_classes:
            pc = permission_class(**self.kwargs)
            if pc.has_permission():
                return True
        return False


class AndResolver(BasePermission):
    def __init__(self, permission_classes, **kwargs):
        super().__init__(**kwargs)
        self.permission_classes = permission_classes

    def has_permission(self):
        for permission_class in self.permission_classes:
            pc = permission_class(**self.kwargs)
            if not pc.has_permission():
                return False
        return True


class NotResolver(BasePermission):
    def __init__(self, permission_class, **kwargs):
        super().__init__(**kwargs)
        self.permission_class = permission_class

    def has_permission(self):
        pc = self.permission_class(**self.kwargs)
        return not pc.has_permission()


class AllowAll(BasePermission):
    def permission_statement(self):
        return True


class AllowNone(BasePermission):
    def permission_statement(self):
        return False
