from django.db.models import Model, CharField, BooleanField, IntegerField


class Book(Model):
    author = CharField(max_length=50)
    title = CharField(max_length=50)
    ISBN = CharField(max_length=13)
    restricted = BooleanField()
    shelf = IntegerField()

    def __str__(self):
        return "{} - {}".format(self.title, self.author)
