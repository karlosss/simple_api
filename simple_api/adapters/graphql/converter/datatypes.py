import datetime

from graphene import Scalar
from graphql.language import ast
from six import string_types


def parse_timedelta(value):
    d = 0
    if " days, " in value:
        value = value.split(" days, ")
        d = int(value[0])
        value = value[1]
    h, m, s = value.split(":")
    h = int(h)
    m = int(m)
    ms = 0
    if "." in s:
        s, ms = s.split(".")
        ms = float("."+ms)*10**6
    s = int(s)
    return datetime.timedelta(days=d, hours=h, minutes=m, seconds=s, microseconds=ms)


class Duration(Scalar):
    """
    The `Duration` scalar type represents a `datetime.timedelta`.
    """
    @staticmethod
    def serialize(td):
        assert isinstance(
            td, datetime.timedelta
        ), 'Received not compatible duration "{}"'.format(repr(td))
        return str(td)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            return cls.parse_value(node.value)

    @staticmethod
    def parse_value(value):
        try:
            if isinstance(value, datetime.timedelta):
                return value
            elif isinstance(value, string_types):
                return parse_timedelta(value)
        except ValueError:
            return None
