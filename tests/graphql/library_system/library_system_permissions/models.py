from django.db.models import Model, EmailField, CharField, TextField, BooleanField, ForeignKey, CASCADE, DecimalField, DateField, PROTECT
from django.contrib.auth.models import User


class Book(Model):
    author = CharField(max_length=50)
    title = CharField(max_length=50)
    ISBN = CharField(max_length=13)
    restricted = BooleanField()
    borrowed = BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.author)


class Subscription(Model):
    start = DateField()
    end = DateField()
    user = ForeignKey(User, on_delete=CASCADE)
