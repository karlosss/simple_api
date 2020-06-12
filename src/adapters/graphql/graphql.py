import graphene

from adapters.base import Adapter
from adapters.graphql.converter.converter import convert_type, convert_function
from adapters.graphql.registry import get_class


class GraphQLAdapter(Adapter):
    def convert_field(self, field, **kwargs):
        return convert_type(field, self, **kwargs)

    def convert_action(self, action):
        params = {}
        for name, field in action.parameters.items():
            params[name] = field.convert(self, input=True)

        field = action.return_value.convert(self, **params)

        def resolve_field(*args, **kwargs):
            return action.exec_fn.convert(self)(*args, **kwargs)

        return field, resolve_field

    def convert_function(self, function, **kwargs):
        return convert_function(function, **kwargs)

    def convert_output_fields_for_object(self, obj):
        out = {}
        for name, field in obj.out_fields.items():
            out[name] = field.convert(self)
        return out

    def convert_input_fields_for_object(self, obj):
        out = {}
        for name, field in obj.in_fields.items():
            out[name] = field.convert(self, input=True)
        return out

    def convert_actions_for_object(self, obj):
        out = {}
        for name, action in obj.actions.items():
            out[name], out["resolve_{}".format(name)] = action.convert(self)
        return out

    def generate(self):
        query_classes = []

        for obj in self.objects:

            for name, field in self.convert_output_fields_for_object(obj).items():
                get_class(obj).output._meta.fields[name] = field

            for name, field in self.convert_input_fields_for_object(obj).items():
                get_class(obj).input._meta.fields[name] = field

            # add actions to per-object query class
            query_class = type("Query", (graphene.ObjectType,), self.convert_actions_for_object(obj))
            query_classes.append(query_class)

        query_class = type("Query", tuple(query_classes) + (graphene.ObjectType,), {})
        return graphene.Schema(query=query_class)
