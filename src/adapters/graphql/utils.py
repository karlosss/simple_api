from enum import Enum


class ConversionType(Enum):
    # type conversions
    OUTPUT = 1
    INPUT = 2
    LIST_OUTPUT = 3
    LIST_INPUT = 4
    PARAMETER = 5

    # function conversions
    EXEC_FN = 6
    RESOLVER = 7


def is_mutation(action):
    return action.kwargs.get("mutation", False)  # todo list of mutation actions
