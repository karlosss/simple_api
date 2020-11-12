# Simple API

## Purpose of the project
After writing Django models, Simple API builds an API (currently, only GraphQL is supported) extracting the information from the model and requiring to write as little code as possible.

Built on some amazing ideas of [graphene-django-extras](https://github.com/eamigo86/graphene-django-extras). The main difference is that Simple API is a bit more high-level and allows the programmer to write even less code.

## User's Guide

### Introduction

Let's build a forum where users can create posts.
The models are as follows:

```python
from django.db.models import Model, EmailField, CharField, TextField, BooleanField, ForeignKey, CASCADE


class CustomUser(Model):
    email = EmailField()
    username = CharField(max_length=50)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    password = CharField(max_length=50)
    bio = TextField()
    is_admin = BooleanField(default=False)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name 
    
    def __str__(self):
        return "{} ({})".format(self.full_name, self.username)


class Post(Model):
    title = CharField(max_length=50)
    author = ForeignKey(CustomUser, on_delete=CASCADE)
    content = TextField()
    
    def __str__(self):
        return "{} by {}".format(self.title, self.author)

```

Now, we create a Simple API object for each model. We also generate GraphQL API and build URL patterns so that we can access the API:

```python
from adapters.graphql.graphql import GraphQLAdapter
from adapters.utils import generate
from django_object.django_object import DjangoObject
from .models import CustomUser as CustomUserModel, Post as PostModel
from tests.graphql.graphql_test_utils import build_patterns


class CustomUser(DjangoObject):
    model = CustomUserModel


class Post(DjangoObject):
    model = PostModel


schema = generate(GraphQLAdapter)
patterns = build_patterns(schema)
``` 

And that's it! Let's explore what Simple API actually generated for us. Open up `/api/` in the browser (i.e. [http://localhost:8000/api/](http://localhost:8000/api/)) and see the schema:

```
// query

PostDetail(id: Int!): Post!
PostList(filters: PostFiltersInput): PostList!
CustomUserDetail(id: Int!): CustomUser!
CustomUserList(filters: CustomUserFiltersInput): CustomUserList!
__objects: [ObjectInfo!]!
__actions: [ActionInfo!]!

// mutation

CustomUserCreate(data: CustomUserCreateInput!): CustomUser!
CustomUserUpdate(data: CustomUserUpdateInput!id: Int!): CustomUser!
CustomUserDelete(id: Int!): Boolean!
PostCreate(data: PostCreateInput!): Post!
PostUpdate(data: PostUpdateInput!id: Int!): Post!
PostDelete(id: Int!): Boolean!
```

With close to zero effort, we just got a way to do list, show detail, create, update and delete both of our entities. Let's try them one by one.

Create a user:

```json
mutation create_user{
  CustomUserCreate(data: {
    email: "user1@example.com", 
    username: "adam", 
    first_name: "Adam", 
    last_name: "First", 
    password: "secret",
    bio: "Just an ordinary person...",
  }){
    id
    email
    username
    first_name
    last_name
    password
    bio
    is_admin
  }
}

// output
{
  "data": {
    "CustomUserCreate": {
      "id": 1,
      "email": "user1@example.com",
      "username": "adam",
      "first_name": "Adam",
      "last_name": "First",
      "password": "secret",
      "bio": "Just an ordinary person...",
      "is_admin": false
    }
  }
}
```

Do a detail of the first user:

```json
query detail_of_user{
  CustomUserDetail(id: 1){
    id
    email
    username
    first_name
    last_name
    password
    bio
    is_admin
  }
}

// output
{
  "data": {
    "CustomUserDetail": {
      "id": 1,
      "email": "user1@example.com",
      "username": "adam",
      "first_name": "Adam",
      "last_name": "First",
      "password": "secret",
      "bio": "Just an ordinary person...",
      "is_admin": false
    }
  }
}
```

The listing action is a bit more interesting. In the schema, we can see there an optional parameter to it, `CustomUserFiltersInput`. Let's explore its fields:

```
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
username: String
username__contains: String
...
ordering: [String!]
```

There are automatically generated filter fields for each of the parameters, and the option to specity the order. Both of those use Django syntax.

Upon return, a listing does not just output a list of objects, but rather a `CustomUserList`, which has the following fields:

```
count: Int!
data(limit: Int = 20, offset: Int = 0): [CustomUser!]!
```

`count` returns the length of the list and `data` holds the actual data, accepting two optional parameters, `limit` and `offset`. This allows for pagination.

Now we can create another user and then list both:

```json
mutation create_another_user{
  CustomUserCreate(data: {
    email: "user2@example.com", 
    username: "bob", 
    first_name: "Bob", 
    last_name: "Second", 
    password: "secret",
    bio: "Just another ordinary person...",
  }){
    id
    email
    username
    first_name
    last_name
    password
    bio
    is_admin
  }
}

query list_users{
  CustomUserList{
    count
    data{
      id
      first_name
      last_name
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 2,
      "data": [
        {
          "id": 1,
          "first_name": "Adam",
          "last_name": "First"
        },
        {
          "id": 2,
          "first_name": "Bob",
          "last_name": "Second"
        }
      ]
    }
  }
}
```

We can also apply some filters to the listing:

```json
query list_filtered_users{
  CustomUserList(filters: {first_name__startswith: "A"}){
    count
    data{
      id
      first_name
      last_name
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 1,
      "data": [
        {
          "id": 1,
          "first_name": "Adam",
          "last_name": "First"
        }
      ]
    }
  }
}
```

Or we can reorder the results: the primary key is the password, which is the same for both, so the secondary key is applied, which is `id` in the descending order:

```json
query list_ordering_users{
  CustomUserList(filters: {ordering: ["password","-id"]}){
    count
    data{
      id
      first_name
      last_name
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 2,
      "data": [
        {
          "id": 2,
          "first_name": "Bob",
          "last_name": "Second"
        },
        {
          "id": 1,
          "first_name": "Adam",
          "last_name": "First"
        }
      ]
    }
  }
}
```

Of course, we can also paginate the results:

```json
query list_paginate_users{
  CustomUserList{
    count
    data(offset: 1, limit: 1){
      id
      first_name
      last_name
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 2,
      "data": [
        {
          "id": 2,
          "first_name": "Bob",
          "last_name": "Second"
        }
      ]
    }
  }
}
```

Next, we can update a user's password like this:

```json
mutation update_password{
  CustomUserUpdate(id: 1, data: {password: "moresecret"}){
    id
    password
  }
}

// output
{
  "data": {
    "CustomUserUpdate": {
      "id": 1,
      "password": "moresecret"
    }
  }
}
```

And we might delete the second user:

```json
mutation delete_user{
  CustomUserDelete(id: 2)
}

// output
{
  "data": {
    "CustomUserDelete": true
  }
}
```

Now, when we list the users again, we can see that there is only one user and the password is changed:

```json
query list_users_with_password{
  CustomUserList{
    count
    data{
      id
      first_name
      last_name
      password
    }
  }
}

// output
{
  "data": {
    "CustomUserList": {
      "count": 1,
      "data": [
        {
          "id": 1,
          "first_name": "Adam",
          "last_name": "First",
          "password": "moresecret"
        }
      ]
    }
  }
}
```

And that concludes the showcase of the basic API. Of course, it is very far from what we would like to run on production - we probably don't want the password to be visible and deleting users should be only possible by admin. But as a starting point, this should be good enough.

### Controlling the fields

### Multiple Objects for one model

### Custom filtering

### Custom actions

### Permissions

### Meta schemas

### Creating Objects without Django model
