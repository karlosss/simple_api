from .objects import schema
from tests.graphql.graphql_test_utils import remove_ws, GraphQLTestCase


class Test(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    REF_GRAPHQL_SCHEMA = """
        schema {
          query: Query
        }
        
        type ActionInfo {
          name: String!
          permitted: Boolean!
          deny_reason: String
          retry_in: Duration
        }
        
        type ContentType {
          id: Int!
          app_label: String!
          model: String!
          logentry_set(filters: LogEntryFiltersInput): LogEntryList!
          permission_set(filters: PermissionFiltersInput): PermissionList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        scalar DateTime
        
        scalar Duration
        
        type Group {
          id: Int!
          name: String!
          permissions(filters: PermissionFiltersInput): PermissionList!
          user_set(filters: UserFiltersInput): UserList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input GroupFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          name: String
          name__contains: String
          name__endswith: String
          name__exact: String
          name__icontains: String
          name__in: [String!]
          name__iregex: String
          name__isnull: Boolean
          name__regex: String
          name__startswith: String
          ordering: [String!]
        }
        
        type GroupList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [Group!]!
        }
        
        type LogEntry {
          id: Int!
          action_time: DateTime!
          object_id: String
          object_repr: String!
          action_flag: Int!
          change_message: String!
          user: User!
          content_type: ContentType
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input LogEntryFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          object_id: String
          object_id__contains: String
          object_id__endswith: String
          object_id__exact: String
          object_id__icontains: String
          object_id__in: [String!]
          object_id__iregex: String
          object_id__isnull: Boolean
          object_id__regex: String
          object_id__startswith: String
          object_repr: String
          object_repr__contains: String
          object_repr__endswith: String
          object_repr__exact: String
          object_repr__icontains: String
          object_repr__in: [String!]
          object_repr__iregex: String
          object_repr__isnull: Boolean
          object_repr__regex: String
          object_repr__startswith: String
          action_flag: Int
          action_flag__exact: Int
          action_flag__gt: Int
          action_flag__gte: Int
          action_flag__in: [Int!]
          action_flag__isnull: Boolean
          action_flag__lt: Int
          action_flag__lte: Int
          change_message: String
          change_message__contains: String
          change_message__endswith: String
          change_message__exact: String
          change_message__icontains: String
          change_message__in: [String!]
          change_message__iregex: String
          change_message__isnull: Boolean
          change_message__regex: String
          change_message__startswith: String
          user_id: Int
          user_id__exact: Int
          user_id__gt: Int
          user_id__gte: Int
          user_id__in: [Int!]
          user_id__isnull: Boolean
          user_id__lt: Int
          user_id__lte: Int
          content_type_id: Int
          content_type_id__exact: Int
          content_type_id__gt: Int
          content_type_id__gte: Int
          content_type_id__in: [Int!]
          content_type_id__isnull: Boolean
          content_type_id__lt: Int
          content_type_id__lte: Int
          ordering: [String!]
        }
        
        type LogEntryList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [LogEntry!]!
        }
        
        type ObjectInfo {
          name: String!
          pk_field: String
          actions: [ActionInfo!]!
        }
        
        type Permission {
          id: Int!
          name: String!
          codename: String!
          content_type: ContentType!
          group_set(filters: GroupFiltersInput): GroupList!
          user_set(filters: UserFiltersInput): UserList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input PermissionFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          name: String
          name__contains: String
          name__endswith: String
          name__exact: String
          name__icontains: String
          name__in: [String!]
          name__iregex: String
          name__isnull: Boolean
          name__regex: String
          name__startswith: String
          codename: String
          codename__contains: String
          codename__endswith: String
          codename__exact: String
          codename__icontains: String
          codename__in: [String!]
          codename__iregex: String
          codename__isnull: Boolean
          codename__regex: String
          codename__startswith: String
          content_type_id: Int
          content_type_id__exact: Int
          content_type_id__gt: Int
          content_type_id__gte: Int
          content_type_id__in: [Int!]
          content_type_id__isnull: Boolean
          content_type_id__lt: Int
          content_type_id__lte: Int
          ordering: [String!]
        }
        
        type PermissionList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [Permission!]!
        }
        
        type Query {
          UserDetail(id: Int!): User!
          UserList(filters: UserFiltersInput): UserList!
          __objects: [ObjectInfo!]!
          __actions: [ActionInfo!]!
        }
        
        type User {
          id: Int!
          password: String!
          last_login: DateTime
          is_superuser: Boolean!
          username: String!
          first_name: String!
          last_name: String!
          email: String!
          is_staff: Boolean!
          is_active: Boolean!
          date_joined: DateTime!
          groups(filters: GroupFiltersInput): GroupList!
          user_permissions(filters: PermissionFiltersInput): PermissionList!
          logentry_set(filters: LogEntryFiltersInput): LogEntryList!
          __str__: String!
          __actions: [ActionInfo!]!
        }
        
        input UserFiltersInput {
          id: Int
          id__exact: Int
          id__gt: Int
          id__gte: Int
          id__in: [Int!]
          id__isnull: Boolean
          id__lt: Int
          id__lte: Int
          password: String
          password__contains: String
          password__endswith: String
          password__exact: String
          password__icontains: String
          password__in: [String!]
          password__iregex: String
          password__isnull: Boolean
          password__regex: String
          password__startswith: String
          username: String
          username__contains: String
          username__endswith: String
          username__exact: String
          username__icontains: String
          username__in: [String!]
          username__iregex: String
          username__isnull: Boolean
          username__regex: String
          username__startswith: String
          first_name: String
          first_name__contains: String
          first_name__endswith: String
          first_name__exact: String
          first_name__icontains: String
          first_name__in: [String!]
          first_name__iregex: String
          first_name__isnull: Boolean
          first_name__regex: String
          first_name__startswith: String
          last_name: String
          last_name__contains: String
          last_name__endswith: String
          last_name__exact: String
          last_name__icontains: String
          last_name__in: [String!]
          last_name__iregex: String
          last_name__isnull: Boolean
          last_name__regex: String
          last_name__startswith: String
          email: String
          email__contains: String
          email__endswith: String
          email__exact: String
          email__icontains: String
          email__in: [String!]
          email__iregex: String
          email__isnull: Boolean
          email__regex: String
          email__startswith: String
          ordering: [String!]
        }
        
        type UserList {
          count: Int!
          data(limit: Int = 20, offset: Int = 0): [User!]!
        }
    """

    REF_META_SCHEMA = {
      "data": {
        "__objects": [
          {
            "name": "User",
            "pk_field": "id",
            "actions": [
              {
                "name": "UserList",
                "permitted": True,
                "deny_reason": None,
                "retry_in": None
              }
            ]
          },
            {
                "name": "Group",
                "pk_field": "id",
                "actions": []
            },
            {
                "name": "Permission",
                "pk_field": "id",
                "actions": []
            },
          {
            "name": "LogEntry",
            "pk_field": "id",
            "actions": []
          },

          {
            "name": "ContentType",
            "pk_field": "id",
            "actions": []
          }
        ],
        "__actions": []
      }
    }
