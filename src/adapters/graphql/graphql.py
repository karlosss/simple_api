import graphene

from adapters.base import Adapter
from adapters.graphql.converter.converter import convert_type, convert_function, ConversionType
from adapters.graphql.registry import get_class, check_classes_for_fields
from adapters.graphql.utils import decapitalize


class GraphQLAdapter(Adapter):
    def convert_field(self, field, **kwargs):
        return convert_type(field, self, **kwargs)

    def convert_action(self, action, **kwargs):
        if action.unsafe:
            return self.convert_unsafe_action(action, kwargs["name"])
        return self.convert_safe_action(action)

    def convert_action_params(self, action):
        params = {}
        for name, field in action.parameters.items():
            params[name] = field.convert(self, _as=ConversionType.PARAMETER)
        return params

    def convert_safe_action(self, action):
        params = self.convert_action_params(action)

        def resolve_field(*args, **kwargs):
            return action.exec_fn.convert(self, _as=ConversionType.EXEC_FN)(*args, **kwargs)

        field = action.return_value.convert(self, _as=ConversionType.OUTPUT, args=params, resolver=resolve_field)

        return field

    def convert_unsafe_action(self, action, name):
        arguments = type("Arguments", (), self.convert_action_params(action))
        output = action.return_value.convert(self, _as=ConversionType.LIST_OUTPUT)

        def mutate(*args, **kwargs):
            return action.exec_fn.convert(self, _as=ConversionType.EXEC_FN)(*args, **kwargs)

        cls = type(name, (graphene.Mutation,), {
            "Arguments": arguments,
            "Output": output,
            "mutate": mutate
        })
        return cls.Field()

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

    def convert_safe_actions(self, actions_dict, prefix=""):
        out = {}
        for name, action in actions_dict.items():
            if prefix:  # add prefix to the action name
                name = decapitalize(prefix) + name.capitalize()
            out[name] = action.convert(self)
        return out

    def convert_actions(self, actions, prefix=""):
        if prefix:
            prefix = decapitalize(prefix) + "_"

        safe_actions = {}
        unsafe_actions = {}

        for name, action in actions.items():
            if action.unsafe:
                unsafe_actions[prefix + name] = self.convert_unsafe_action(action, prefix+name)
            else:
                safe_actions[prefix + name] = self.convert_safe_action(action)

        return safe_actions, unsafe_actions

    @staticmethod
    def update_mutation_classes(unsafe_actions, mutation_classes):
        for name, action in unsafe_actions.items():
            assert name not in mutation_classes, "Duplicate unsafe action name: `{}`".format(name)
            mutation_classes[name] = action

    def generate(self):
        query_classes = []
        mutation_classes = {}

        at_least_one_action_exists = False

        for obj in self.objects:
            for name, field in self.convert_output_fields_for_object(obj).items():
                get_class(obj)._meta.fields[name] = field

            for name, field in self.convert_input_fields_for_object(obj).items():
                get_class(obj, input=True)._meta.fields[name] = field

            safe_actions, unsafe_actions = self.convert_actions(obj.actions, obj.__name__)
            if safe_actions:
                at_least_one_action_exists = True

            query_class = type("Query", (graphene.ObjectType,), safe_actions)
            query_classes.append(query_class)
            self.update_mutation_classes(unsafe_actions, mutation_classes)

        safe_actions, unsafe_actions = self.convert_actions(self.extra_actions)
        if safe_actions:
            at_least_one_action_exists = True

        self.update_mutation_classes(unsafe_actions, mutation_classes)

        assert at_least_one_action_exists, "At least one safe action must exist in the API."

        query_class = type("Query", tuple(query_classes) + (graphene.ObjectType,), safe_actions)

        mutation_class = None
        if mutation_classes:
            mutation_class = type("Mutation", (graphene.ObjectType,), mutation_classes)

        check_classes_for_fields()
        return graphene.Schema(query=query_class, mutation=mutation_class)
