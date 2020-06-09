from adapters.graphql.converter.convert_input_type import convert_input_type
from adapters.graphql.converter.convert_list_input_type import convert_list_input_type
from adapters.graphql.converter.convert_list_output_type import convert_list_output_type
from adapters.graphql.converter.convert_output_type import convert_output_type
from adapters.graphql.utils import in_kwargs_and_true


def convert_type(type, adapter, **kwargs):
    if not in_kwargs_and_true("input", kwargs) and not in_kwargs_and_true("list", kwargs):
        return convert_output_type(type, adapter, **kwargs)
    if in_kwargs_and_true("input", kwargs) and not in_kwargs_and_true("list", kwargs):
        kwargs.pop("input")
        return convert_input_type(type, adapter, **kwargs)
    if not in_kwargs_and_true("input", kwargs) and in_kwargs_and_true("list", kwargs):
        kwargs.pop("list")
        return convert_list_output_type(type, adapter, **kwargs)
    if in_kwargs_and_true("input", kwargs) and in_kwargs_and_true("list", kwargs):
        kwargs.pop("input")
        kwargs.pop("list")
        return convert_list_input_type(type, adapter, **kwargs)
