from django.core.exceptions import ValidationError
from django.db.models import Model, CharField, BooleanField, IntegerField, ForeignKey, CASCADE


def shelf_Validator(value):
    if value <= 0 or value == 7:
        raise ValidationError('%(value)s is not valid shelf number', params={'value': value})


class Book(Model):
    author = CharField(max_length=50)
    title = CharField(max_length=50)
    ISBN = CharField(max_length=13)
    restricted = BooleanField()
    shelf = IntegerField(validators=[shelf_Validator])

    def __str__(self):
        return "{} - {}".format(self.title, self.author)


class Bookmark(Model):
    page = IntegerField()
    book = ForeignKey(Book, CASCADE)
