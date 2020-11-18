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
