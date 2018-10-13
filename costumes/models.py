from django.db import models

# vzor_kostymu
class CostumeTemplate(models.Model):
    costume_type = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return 'CostumeTemplate = ' + 'costume_type: ' + self.costume_type + 'manufacturer: ' + self.manufacturer + 'material: ' + self.material + 'description: ' + self.description
# doplnok
class Accessory(models.Model):
    name = models.CharField(max_length=100)
    manufactured = models.DateTimeField('date created')
    description = models.CharField(max_length=500)

    def __str__(self):
        return 'Accessory = ' + 'name: ' + self.name + 'manufactured: ' + self.manufactured + 'description: ' + self.description

# klient
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    # TODO: is CharField the right type for this variable?
    tel_num = models.CharField(max_length=10)

    def __str__(self):
        return 'Customer = ' + 'first_name: ' + self.first_name + 'second_name: ' + self.second_name + 'address: ' + self.address + 'email: ' + self.email + 'tel_num: ' + self.tel_num
