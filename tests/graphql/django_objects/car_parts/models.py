from django.db.models import Model, IntegerField, TextField, CharField, ForeignKey, CASCADE


class Manufacturer(Model):
    name = CharField(max_length=50)


class Car(Model):
    number_plate = CharField(max_length=10, primary_key=True)


class Wheel(Model):
    car = ForeignKey(Car, blank=True, null=True, on_delete=CASCADE)
    manufacturer = ForeignKey(Manufacturer, on_delete=CASCADE)


class Exhaust(Model):
    car = ForeignKey(Car, blank=True, null=True, on_delete=CASCADE)
