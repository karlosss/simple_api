import graphene

from adapters.base import Adapter
from adapters.graphql.converter.converter import convert_type, convert_function, ConversionType
from adapters.graphql.registry import get_class, check_classes_for_fields
from adapters.graphql.utils import decapitalize, is_mutation
from object.actions import Action
from object.datatypes import BooleanType
from object.function import Function


class GraphQLAdapter(Adapter):
    def convert_field(self, field, **kwargs):
        return convert_type(field, self, **kwargs)

    def convert_action(self, action, **kwargs):
        if is_mutation(action):
            return self.convert_mutation_action(action, kwargs["name"])
        return self.convert_query_action(action)

    def convert_action_params(self, action):
        params = {}
        for name, field in action.parameters.items():
            params[name] = field.convert(self, _as=ConversionType.PARAMETER)
        return params

    def convert_query_action(self, action):
        params = self.convert_action_params(action)

        def resolve_field(*args, **kwargs):
            return action.get_exec_fn().convert(self, _as=ConversionType.EXEC_FN)(*args, **kwargs)

        field = action.get_return_value().convert(self, _as=ConversionType.OUTPUT, args=params, resolver=resolve_field)

        return field

    def convert_mutation_action(self, action, name):
        arguments = type("Arguments", (), self.convert_action_params(action))
        output = action.get_return_value().convert(self, _as=ConversionType.LIST_OUTPUT)

        def mutate(*args, **kwargs):
            return action.get_exec_fn().convert(self, _as=ConversionType.EXEC_FN)(*args, **kwargs)

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

    def convert_query_actions(self, actions_dict, prefix=""):
        out = {}
        for name, action in actions_dict.items():
            if prefix:  # add prefix to the action name
                name = decapitalize(prefix) + name.capitalize()
            out[name] = action.convert(self)
        return out

    def convert_actions(self, actions, prefix=""):
        if prefix:
            prefix = decapitalize(prefix) + "_"

        query_actions = {}
        mutation_actions = {}

        for name, action in actions.items():
            converted_action = action.convert(self, name=prefix+name)
            if is_mutation(action):
                mutation_actions[prefix + name] = converted_action
            else:
                query_actions[prefix + name] = converted_action

        return query_actions, mutation_actions

    @staticmethod
    def update_mutation_classes(mutation_actions, mutation_classes):
        for name, action in mutation_actions.items():
            assert name not in mutation_classes, "Duplicate mutation action name: `{}`".format(name)
            mutation_classes[name] = action

    def generate(self):
        query_classes = []
        mutation_classes = {}

        at_least_one_query_action_exists = False

        for obj in self.objects:
            for name, field in self.convert_output_fields_for_object(obj).items():
                get_class(obj)._meta.fields[name] = field

            for name, field in self.convert_input_fields_for_object(obj).items():
                get_class(obj, input=True)._meta.fields[name] = field

            query_actions, mutation_actions = self.convert_actions(obj.actions, obj.__name__)
            if query_actions:
                at_least_one_query_action_exists = True

            query_class = type("Query", (graphene.ObjectType,), query_actions)
            query_classes.append(query_class)
            self.update_mutation_classes(mutation_actions, mutation_classes)

        query_actions, mutation_actions = self.convert_actions(self.extra_actions)
        
        # if there are no query actions, create a dummy one, since graphene-python needs that
        if not query_actions and not at_least_one_query_action_exists:
            query_actions = {"dummy": Action(return_value=BooleanType(),
                                             exec_fn=Function(lambda request, params: False)).convert(self)}

        self.update_mutation_classes(mutation_actions, mutation_classes)

        query_class = type("Query", tuple(query_classes) + (graphene.ObjectType,), query_actions)

        mutation_class = None
        if mutation_classes:
            mutation_class = type("Mutation", (graphene.ObjectType,), mutation_classes)

        check_classes_for_fields()
        return graphene.Schema(query=query_class, mutation=mutation_class)
