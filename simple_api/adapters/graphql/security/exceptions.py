class ResourceLimitReached(Exception):
    pass


class QueryWeightExceeded(ResourceLimitReached):
    pass


class DepthLimitReached(ResourceLimitReached):
    pass


class ListLimitRequired(ResourceLimitReached):
    pass


class ListLimitTooHigh(ResourceLimitReached):
    pass
