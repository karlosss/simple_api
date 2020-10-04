from django.db.models import Model, IntegerField, CharField, ForeignKey, CASCADE


class Person(Model):
    age = IntegerField()


class Car(Model):
    brand = CharField(max_length=50)
    owner = ForeignKey(Person, CASCADE)
