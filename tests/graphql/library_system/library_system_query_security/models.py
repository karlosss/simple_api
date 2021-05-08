from django.db.models import Model, IntegerField, ForeignKey, CASCADE


class Book(Model):
    shelf = IntegerField()


class Bookmark(Model):
    page = IntegerField()
    book = ForeignKey(Book, CASCADE)
