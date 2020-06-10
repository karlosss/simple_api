from adapters.graphql.converter.convert_function import convert_function_as_field_resolver, convert_function_as_exec_fn
from adapters.graphql.converter.convert_input_type import convert_input_type
from adapters.graphql.converter.convert_list_input_type import convert_list_input_type
from adapters.graphql.converter.convert_list_output_type import convert_list_output_type
from adapters.graphql.converter.convert_output_type import convert_output_type
from adapters.graphql.utils import in_kwargs_and_true


def check_no_params_and_resolver(type):
    assert not type.parameters and type.resolver is None, \
        "Cannot set parameters nor resolver for input and/or list type."


def convert_type(type, adapter, **kwargs):
    if not in_kwargs_and_true("input", kwargs) and not in_kwargs_and_true("list", kwargs):
        return convert_output_type(type, adapter, **kwargs)

    if in_kwargs_and_true("input", kwargs) and not in_kwargs_and_true("list", kwargs):
        kwargs.pop("input")
        check_no_params_and_resolver(type)
        return convert_input_type(type, adapter, **kwargs)

    if not in_kwargs_and_true("input", kwargs) and in_kwargs_and_true("list", kwargs):
        kwargs.pop("list")
        check_no_params_and_resolver(type)
        return convert_list_output_type(type, adapter, **kwargs)

    if in_kwargs_and_true("input", kwargs) and in_kwargs_and_true("list", kwargs):
        kwargs.pop("input")
        kwargs.pop("list")
        check_no_params_and_resolver(type)
        return convert_list_input_type(type, adapter, **kwargs)


def convert_function(function, **kwargs):
    if in_kwargs_and_true("resolver", kwargs):
        kwargs.pop("resolver")
        return convert_function_as_field_resolver(function)
    else:
        return convert_function_as_exec_fn(function)
