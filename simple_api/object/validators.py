from inspect import isclass


def build_validation_fn(action_validators, parameter_validators, data_validators):
    """
    Prepares function for validation of input values and the action overall, instantiates validators which are not
    already instantiated. Action_validators can be a sigle validator, Field_validators a List of tuples
    (string, (validators...)) as prepared in object/actions.py
    """
    ins_action_validators = []
    ins_parameter_validators = {}
    ins_data_validators = {}

    # Validators instantiation if they are not already
    for cls_or_inst in action_validators:
        if isclass(cls_or_inst):
            ins_action_validators.append(cls_or_inst())
        else:
            ins_action_validators.append(cls_or_inst)
    for parameter_field, parameter_validators in parameter_validators.items():
        for validator in parameter_validators:
            if isclass(validator):
                ins_parameter_validators.setdefault(parameter_field, []).append(validator())
            else:
                ins_parameter_validators.setdefault(parameter_field, []).append(validator)
    for data_field, data_validators in data_validators.items():
        for validator in data_validators:
            if isclass(validator):
                ins_data_validators.setdefault(data_field, []).append(validator())
            else:
                ins_data_validators.setdefault(data_field, []).append(validator)

    def fn(**kwargs):
        # Action validators
        for valid in ins_action_validators:
            if not valid.validation_statement(**kwargs):
                raise ValueError(valid.error_message(**kwargs))
        # Parameters validators
        for param_field, validators in ins_parameter_validators.items():
            for validator in validators:
                if not validator.validation_statement(kwargs["request"], value=kwargs["params"][param_field]):
                    raise ValueError(validator.error_message(**kwargs))
        # Data validators
        for data_field, validators in ins_data_validators.items():
            for validator in validators:
                if not validator.validation_statement(kwargs["request"], value=kwargs["params"]["data"][data_field]):
                    raise ValueError(validator.error_message(**kwargs))
    return fn


class Validator:
    """
    Base class for input field validation, validation itself is done withing validation_statement(self, value,
    **kwargs)
    """

    def validation_statement(self, request, value=None, **kwargs):
        """Function to validate input value, True -> input is valid, False -> invalid"""
        raise NotImplementedError

    def error_message(self, **kwargs):
        """Message to return in API when validation fails"""
        return "Validation failed in FieldValidator"
