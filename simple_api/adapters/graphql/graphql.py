import graphene

from simple_api.adapters.base import Adapter
from simple_api.adapters.graphql.constants import INPUT_CLASS_SUFFIX
from simple_api.adapters.graphql.converter.converter import convert_type, convert_function, ConversionType
from simple_api.adapters.graphql.registry import get_class, check_classes_for_fields
from simple_api.adapters.graphql.utils import is_mutation, capitalize
from simple_api.object.actions import Action
from simple_api.object.datatypes import BooleanType
from simple_api.object.function import Function


class GraphQLAdapter(Adapter):
    def convert_field(self, field, **kwargs):
        return convert_type(field, self, **kwargs)

    def convert_action(self, action, **kwargs):
        if is_mutation(action):
            return self.convert_mutation_action(action, kwargs["name"])
        return self.convert_query_action(action)

    def convert_action_params_and_data(self, action):
        params = {}
        for name, field in action.parameters.items():
            params[name] = field.convert(self, _as=ConversionType.PARAMETER)

        # we need to convert data here manually to avoid creating new Objects, which would chance the set over
        # which the generate() function currently iterates
        if action.data:
            data_params = {}
            for name, field in action.data.items():
                data_params[name] = field.convert(self, _as=ConversionType.INPUT)
            cls = type("{}{}{}".format(action.parent_class.__name__ if action.parent_class is not None else "", capitalize(action.name), INPUT_CLASS_SUFFIX),
                       (graphene.InputObjectType,), data_params)
            params["data"] = graphene.Argument(cls, required=True)
        return params

    def convert_query_action(self, action):
        params = self.convert_action_params_and_data(action)

        def resolve_field(*args, **kwargs):
            return action.get_fn().convert(self, _as=ConversionType.EXEC_FN)(*args, **kwargs)

        field = action.get_return_value().convert(self, _as=ConversionType.OUTPUT, args=params, resolver=resolve_field)

        return field

    def convert_mutation_action(self, action, name):
        arguments = type("Arguments", (), self.convert_action_params_and_data(action))
        output = action.get_return_value().convert(self, _as=ConversionType.LIST_OUTPUT)

        def mutate(*args, **kwargs):
            return action.get_fn().convert(self, _as=ConversionType.EXEC_FN)(*args, **kwargs)

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
            if prefix:
                name = prefix + capitalize(name)
            out[name] = action.convert(self)
        return out

    def convert_actions(self, actions, prefix=""):
        query_actions = {}
        mutation_actions = {}

        for name, action in actions.items():
            if prefix:
                name = prefix + capitalize(name)
            converted_action = action.convert(self, name=name)
            if is_mutation(action):
                mutation_actions[name] = converted_action
            else:
                query_actions[name] = converted_action

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
        return graphene.Schema(query=query_class, mutation=mutation_class, auto_camelcase=False)
