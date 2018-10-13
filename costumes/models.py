from django.db import models

# vzor_kostymu
class CostumeTemplate(models.Model):
    costume_type = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

# doplnok
class Accessory(models.Model):
    name = models.CharField(max_length=100)
    manufactured = models.DateTimeField('date created')
    description = models.CharField(max_length=500)

# klient
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    # TODO: is CharField the right type for this variable?
    tel_num = models.CharField(max_length=10)
