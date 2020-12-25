from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, ForeignKey, CASCADE


class Post(Model):
    title = CharField(max_length=50)
    author = ForeignKey(User, on_delete=CASCADE)
    content = TextField()

    def __str__(self):
        return "{} by {}".format(self.title, self.author)
