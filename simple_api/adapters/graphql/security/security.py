from graphql.backend.core import GraphQLCoreBackend
from graphql.language.ast import OperationDefinition, FragmentDefinition, FragmentSpread, IntValue

from simple_api.adapters.graphql.security.exceptions import *


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


def preflight_query_check(
        selection_set, fragments,
        depth_limit, node_limit, list_limit,
        depth_level=1):
    nodes = 0
    current_max_depth = depth_level
    if depth_limit and current_max_depth > depth_limit:
        raise DepthLimitReached("Query depth limit exceeded")
    for field in selection_set.selections:
        if isinstance(field, FragmentSpread):
            field = fragments.get(field.name.value)
        if field.selection_set:
            # Recursive check for node amount and depth of query
            new_depth, local_nodes = \
                preflight_query_check(
                    field.selection_set,
                    fragments,
                    depth_limit,
                    node_limit,
                    list_limit,
                    depth_level=depth_level + 1)
            # Data selection must be limited
            if field.name.value == "data":
                limit = get_limit_if_exists(field.arguments)
                if limit:
                    if isinstance(limit.value, IntValue):
                        limit_value = int(limit.value.value)
                        if limit_value > list_limit:
                            raise ListLimitTooHigh("Number of items requested must be below " + str(list_limit))
                        nodes += local_nodes * limit_value
                else:
                    raise ListLimitRequired("Requests for paginated data require limit")
            else:
                nodes += local_nodes + 1
            if node_limit and nodes > node_limit:
                raise SelectionsLimitReached("Query uses too many nodes")
            if new_depth > current_max_depth:
                current_max_depth = new_depth
        else:
            nodes += 1
    return current_max_depth, nodes


class PreflightQueryManager(GraphQLCoreBackend):
    def __init__(self, *args, depth_limit=10, node_limit=1000, list_limit=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.depth_limit = depth_limit
        self.node_limit = node_limit
        self.list_limit = list_limit

    def document_from_string(self, schema, document_string):
        # let GraphQLCoreBackend munch
        document = super().document_from_string(schema, document_string)
        ast = document.document_ast
        # fragments are like a dictionary of views
        fragments = get_fragments(ast.definitions)
        for definition in ast.definitions:

            # Check if definition is query or mutations
            if not isinstance(definition, OperationDefinition):
                continue

            preflight_query_check(
                definition.selection_set,
                fragments,
                self.depth_limit,
                self.node_limit,
                self.list_limit
            )
        return document

