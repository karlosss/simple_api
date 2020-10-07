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


class Permission:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def has_permission(self, *args, **kwargs):
        raise NotImplementedError

    def error_message(self):
        return "You do not have permission to access this."


class AllowAll(Permission):
    def has_permission(self, *args, **kwargs):
        return True


class AllowNone(Permission):
    def has_permission(self, *args, **kwargs):
        return False
