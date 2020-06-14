import graphene

from adapters.base import Adapter
from adapters.graphql.converter.converter import convert_type, convert_function, ConversionType
from adapters.graphql.registry import get_class, check_classes_for_fields
from adapters.graphql.utils import decapitalize


class GraphQLAdapter(Adapter):
    def convert_field(self, field, **kwargs):
        return convert_type(field, self, **kwargs)

    def convert_action(self, action):
        params = {}
        for name, field in action.parameters.items():
            params[name] = field.convert(self, _as=ConversionType.PARAMETER)

        field = action.return_value.convert(self, _as=ConversionType.OUTPUT, args=params)

        def resolve_field(*args, **kwargs):
            return action.exec_fn.convert(self, _as=ConversionType.EXEC_FN)(*args, **kwargs)

        return field, resolve_field

    def convert_function(self, function, **kwargs):
        return convert_function(function, **kwargs)

    def convert_output_fields_for_object(self, obj):
        out = {}
        for name, field in obj.out_fields.items():
            out[name] = field.convert(self, _as=ConversionType.OUTPUT)
        return out

    def convert_input_fields_for_object(self, obj):
        out = {}
        for name, field in obj.in_fields.items():
            out[name] = field.convert(self, _as=ConversionType.INPUT)
        return out

    def convert_actions(self, actions_dict, prefix=""):
        out = {}
        for name, action in actions_dict.items():
            if prefix:  # add prefix to the action name
                name = decapitalize(prefix) + name.capitalize()
            out[name], out["resolve_{}".format(name)] = action.convert(self)
        return out

    def generate(self):
        query_classes = []

        at_least_one_action_exists = False

        for obj in self.objects:

            for name, field in self.convert_output_fields_for_object(obj).items():
                get_class(obj)._meta.fields[name] = field

            for name, field in self.convert_input_fields_for_object(obj).items():
                get_class(obj, input=True)._meta.fields[name] = field

            # add actions to per-object query class
            actions = self.convert_actions(obj.actions, prefix=obj.__name__)
            if actions:
                at_least_one_action_exists = True
            query_class = type("Query", (graphene.ObjectType,), actions)
            query_classes.append(query_class)

        extra_actions = self.convert_actions(self.extra_actions)
        if extra_actions:
            at_least_one_action_exists = True

        assert at_least_one_action_exists, "At least one action must exist in the API."

        query_class = type("Query", tuple(query_classes) + (graphene.ObjectType,), extra_actions)
        check_classes_for_fields()
        return graphene.Schema(query=query_class)
