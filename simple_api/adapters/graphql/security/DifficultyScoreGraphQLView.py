import re

from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from graphene_django.views import GraphQLView, HttpError
from graphql.execution import ExecutionResult
from graphql.language.ast import FragmentDefinition, FragmentSpread, OperationDefinition, IntValue

from simple_api.adapters.graphql.security.exceptions import ListLimitRequired, ListLimitTooHigh, QueryWeightExceeded, \
    DepthLimitReached, ActionsLimitExceeded


def parse_paginated_list_type(list_type_name):
    found_type = re.findall(r"Paginated\[(\S+)]", list_type_name)
    if len(found_type) == 1:
        return found_type[0]
    else:
        return None


def ignore_notNull(object_type):
    if object_type[-1] == "!":
        return object_type[:-1]
    return object_type


def get_fragments(definitions):
    return {
        definition.name.value: definition
        for definition in definitions
        if isinstance(definition, FragmentDefinition)
    }


def get_limit_if_exists(arguments):
    for x in arguments:
        if x.name.value == "limit":
            return x
    return None


class DifficultyScoreGraphQlView(GraphQLView):
    sec_weight_schema = None
    list_limit = None
    weight_limit = None
    depth_limit = None
    action_limit=None
    default_expected_list_size = 20

    def __init__(self, *args,
                 sec_weight_schema=None,
                 list_limit=None,
                 weight_limit=None,
                 depth_limit=None,
                 action_limit=None,
                 default_expected_list_size=20, **kwargs):
        self.sec_weight_schema = sec_weight_schema
        self.list_limit = list_limit
        self.weight_limit = weight_limit
        self.depth_limit = depth_limit
        self.action_limit = action_limit
        self.default_expected_list_size = default_expected_list_size
        super().__init__(*args, **kwargs)

    def execute_graphql_request(
            self, request, data, query, variables, operation_name, show_graphiql=False
    ):
        """
        Largely a copy of GraphQLView execute_graphql_request function, the check has to happen in the middle of its
        processing so whole function needs to be replicated here
        """
        if not query:
            if show_graphiql:
                return None
            raise HttpError(HttpResponseBadRequest("Must provide query string."))

        try:
            backend = self.get_backend(request)
            document = backend.document_from_string(self.schema, query)
        except Exception as e:
            return ExecutionResult(errors=[e], invalid=True)

        if request.method.lower() == "get":
            operation_type = document.get_operation_type(operation_name)
            if operation_type and operation_type != "query":
                if show_graphiql:
                    return None

                raise HttpError(
                    HttpResponseNotAllowed(
                        ["POST"],
                        "Can only perform a {} operation from a POST request.".format(
                            operation_type
                        ),
                    )
                )

        # Check request weight
        try:
            if self.list_limit or self.weight_limit or self.depth_limit:
                if document:
                    fragments = get_fragments(document.document_ast.definitions)
                    definitions_total_weight = 0
                    total_actions = 0
                    for definition in document.document_ast.definitions:
                        if not isinstance(definition, OperationDefinition):
                            continue

                        def_weight, additional_actions = self.calculate_action_score(
                            definition.selection_set,
                            fragments)
                        total_actions += additional_actions
                        definitions_total_weight += def_weight
                        if self.weight_limit and definitions_total_weight > self.weight_limit:
                            raise QueryWeightExceeded("Your query exceeds the maximum query weight allowed")
                        if self.action_limit and total_actions > self.action_limit:
                            raise ActionsLimitExceeded("Your request contains too many actions")
        except Exception as e:
            return ExecutionResult(errors=[e], invalid=True)

        try:
            extra_options = {}
            if self.executor:
                # We only include it optionally since
                # executor is not a valid argument in all backends
                extra_options["executor"] = self.executor

            return document.execute(
                root_value=self.get_root_value(request),
                variable_values=variables,
                operation_name=operation_name,
                context_value=self.get_context(request),
                middleware=self.get_middleware(request),
                **extra_options
            )
        except Exception as e:
            return ExecutionResult(errors=[e], invalid=True)

    def calculate_action_score(self, selection_set, fragments, depth_level=1):
        """
        For every action, add up the cost of its fields it expects
        from its return and then multiply it by its own weight.
        """
        total_weight = 0
        total_actions = 0
        if self.depth_limit and depth_level > self.depth_limit:
            raise DepthLimitReached("Query depth limit exceeded")
        # Take every action from selection_set
        for action in selection_set.selections:
            if isinstance(action, FragmentSpread):
                action = fragments.get(action.name.value)
            # add to action amount
            total_actions += 1
            if self.action_limit and total_actions > self.action_limit:
                raise ActionsLimitExceeded("Your request contains too many actions")
            # Get action return type
            actionDetails = self.sec_weight_schema["actions"][action.name.value]

            if action.selection_set:
                total_weight += actionDetails["weight"]
                total_weight += self.calculate_field_score(actionDetails["returnType"],
                                                           action.selection_set,
                                                           fragments)
            else:
                total_weight += actionDetails["weight"]
            if self.weight_limit and total_weight > self.weight_limit:
                raise QueryWeightExceeded("Your query exceeds the maximum query weight allowed")
        if self.weight_limit and total_weight > self.weight_limit:
            raise QueryWeightExceeded("Your query exceeds the maximum query weight allowed")
        return total_weight, total_actions

    def calculate_field_score(self, object_type, selection_set, fragments, depth_level=1):
        total_weight = 0
        if self.depth_limit and depth_level > self.depth_limit:
            raise DepthLimitReached("Query depth limit exceeded")
        # Is Paginated list?
        is_list = parse_paginated_list_type(object_type)
        if is_list:
            return self.calculate_list_score(is_list, selection_set, fragments, depth_level)
        object_type = ignore_notNull(object_type)
        if object_type not in self.sec_weight_schema["types"]:
            return 0
        type_fields = self.sec_weight_schema["types"][object_type]
        for field in selection_set.selections:
            # Check for fragments again
            if isinstance(field, FragmentSpread):
                field = fragments.get(field.name.value)
            # Does this selection get non-primitive type?
            if field.name.value in type_fields["connected"]:
                # Does part of selection result in a list?
                is_list = parse_paginated_list_type(type_fields["connected"][field.name.value])
                if is_list:
                    list_weight = self.calculate_list_score(is_list,
                                                            field.selection_set,
                                                            fragments,
                                                            depth_level + 1)
                    total_weight += type_fields["direct"][field.name.value] * list_weight
                else:
                    total_weight += self.calculate_field_score(type_fields["connected"][field.name.value],
                                                               field.selection_set,
                                                               fragments,
                                                               depth_level + 1)
            else:
                total_weight += type_fields["direct"][field.name.value]
        if self.weight_limit and total_weight > self.weight_limit:
            raise QueryWeightExceeded("Your query exceeds the maximum query weight allowed")
        return total_weight

    def calculate_list_score(self, data_object_type, selection_set, fragments, depth_level=1):
        total_weight = 0
        if self.depth_limit and depth_level > self.depth_limit:
            raise DepthLimitReached("Query depth limit exceeded")
        for field in selection_set.selections:
            # Checking for limit here prevents missing on field named data not in paginated list
            if field.name.value == "data":
                limit = get_limit_if_exists(field.arguments)
                limit_value = self.default_expected_list_size
                # Check for limit
                if self.list_limit and limit:
                    if isinstance(limit.value, IntValue):
                        limit_value = int(limit.value.value)
                        if limit_value > self.list_limit:
                            raise ListLimitTooHigh(
                                "Number of items requested must be below " + str(self.list_limit))
                else:
                    raise ListLimitRequired("Requests for paginated data require limit")
                # Calculate cost for subselections
                weight_of_subselections = self.calculate_field_score(data_object_type, field.selection_set, fragments,
                                                                     depth_level + 1)
                total_weight += weight_of_subselections * limit_value
            else:
                total_weight += 1
        if self.weight_limit and total_weight > self.weight_limit:
            raise QueryWeightExceeded("Your query exceeds the maximum query weight allowed")
        return total_weight
