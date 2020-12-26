from simple_api.adapters.graphql.converter.convert_parameter_type import convert_parameter_type
from simple_api.adapters.graphql.converter.convert_function import convert_function_as_field_resolver, convert_function_as_exec_fn
from simple_api.adapters.graphql.converter.convert_input_type import convert_input_type
from simple_api.adapters.graphql.converter.convert_list_input_type import convert_list_input_type
from simple_api.adapters.graphql.converter.convert_list_output_type import convert_list_output_type
from simple_api.adapters.graphql.converter.convert_output_type import convert_output_type
from simple_api.adapters.graphql.utils import ConversionType


def check_no_params_and_resolver(type):
    assert not type.parameters and type.resolver is None, \
        "Cannot set parameters nor resolver for input and/or list type."


def convert_type(type, adapter, _as, **kwargs):
    if _as == ConversionType.PARAMETER:
        return convert_parameter_type(type, adapter, **kwargs)

    if _as == ConversionType.OUTPUT:
        return convert_output_type(type, adapter, **kwargs)

    if _as == ConversionType.INPUT:
        return convert_input_type(type, adapter, **kwargs)

    if _as == ConversionType.LIST_OUTPUT:
        return convert_list_output_type(type, adapter, **kwargs)

    if _as == ConversionType.LIST_INPUT:
        return convert_list_input_type(type, adapter, **kwargs)

    assert False, "Unknown conversion type: `{}`".format(_as)


def convert_function(function, _as, **kwargs):
    if _as == ConversionType.EXEC_FN:
        return convert_function_as_exec_fn(function)

    if _as == ConversionType.RESOLVER:
        return convert_function_as_field_resolver(function)

    assert False, "Unknown conversion type: `{}`".format(_as)

