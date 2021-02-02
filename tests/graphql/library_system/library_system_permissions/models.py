from django.db.models import Model, EmailField, CharField, TextField, BooleanField, ForeignKey, CASCADE, DecimalField, DateField, PROTECT


class CustomUser(Model):
    email = EmailField()
    username = CharField(max_length=50)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    password = CharField(max_length=50)
    bio = TextField()
    is_admin = BooleanField(default=False)
    can_lend = BooleanField(default=False)
    can_return = BooleanField(default=False)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return "{} ({})".format(self.full_name, self.username)


class Book(Model):
    author = CharField(max_length=50)
    title = CharField(max_length=50)
    ISBN = CharField(max_length=13)
    restricted = BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.author)


class Subscription(Model):
    start = DateField()
    end = DateField()
    user = ForeignKey(CustomUser, on_delete=CASCADE)


class Lease(Model):
    book = ForeignKey(Book, on_delete=PROTECT)
    borrower = ForeignKey(CustomUser, on_delete=PROTECT)
    start = DateField()
    end = DateField()
