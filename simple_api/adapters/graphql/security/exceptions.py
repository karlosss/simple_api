class ResourceLimitReached(Exception):
    pass


class DepthLimitReached(ResourceLimitReached):
    pass


class SelectionsLimitReached(ResourceLimitReached):
    pass


class ListLimitRequired(ResourceLimitReached):
    pass


class ListLimitTooHigh(ResourceLimitReached):
    pass
