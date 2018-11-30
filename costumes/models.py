from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# pobocka
class Store(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    num = models.CharField(max_length=100)
    opened_from = models.CharField(max_length=5, default='08:00')
    opened_to = models.CharField(max_length=5, default='18:00')

    def __str__(self):
        return 'Store = ' + ' street: ' + self.street + ' city: ' + self.city + ' opened_from: ' + self.opened_from + ' opened_to: ' + self.opened_to

# vzor_kostymu
class CostumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return 'CostumeTemplate = ' + ' name: ' + self.name + ' manufacturer: ' + self.manufacturer + ' material: ' + self.material + ' description: ' + self.description

# doplnok
class Accessory(models.Model):
    name = models.CharField(max_length=100)
    manufactured = models.DateField('date created')
    description = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='accessory_images/', default='default_images/default.png')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=1)
    belongs_to_costume = models.ManyToManyField(CostumeTemplate, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return 'Accessory = ' + ' name: ' + self.name + ' manufactured: ' + str(self.manufactured) + ' description: ' + self.description + ' price: ' + str(self.price)

# klient
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    tel_num = models.CharField(max_length=15)

    def __str__(self):
        return 'Customer = ' +  ' address: ' + self.address + ' tel_num: ' + self.tel_num

# zamestnanec
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    tel_num = models.CharField(max_length=10)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Employee = ' +  ' address: ' + self.address + ' tel_num: ' + self.tel_num

# spravca
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100)
    tel_num = models.CharField(max_length=10)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Manager = ' +  ' address: ' + self.address + ' tel_num: ' + self.tel_num

# kostym
class Costume(models.Model):
    COSTUME_SIZE = (
        ('XS', 'XS - Extra Small'),
        ('S', 'S - Small'),
        ('M', 'M - Medium'),
        ('L', 'L - Large'),
        ('XL', 'XL - Extra Large'),
        ('XXL', 'XXL - Extra Extra Large'),
    )
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=3, choices=COSTUME_SIZE)
    manufactured = models.DateField('date created')
    wear_out = models.CharField(max_length=100)
    employee_manage = models.ForeignKey(Employee, on_delete=models.CASCADE)
    costume_template = models.ForeignKey(CostumeTemplate, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='costume_images/', default='default_images/default.png')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=1)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return 'Costume = ' + ' color: ' + self.color + ' size: ' + self.size + ' manufactured: ' + str(self.manufactured) + ' wear_out: ' + self.wear_out + ' employee_manage: ' + str(self.employee_manage) + ' costume_template: ' + str(self.costume_template) + ' store: ' + str(self.store)

# vypozicka
class Borrowing(models.Model):
    event = models.CharField(max_length=100, blank=True)
    borrowed_date = models.DateField('time borrowed')
    return_date = models.DateField('date to return', blank=True, null=True)
    borrowing_expiration = models.DurationField('borrowed for duration')
    final_price = models.IntegerField(default=0)
    employee_borrowed = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    costume = models.ManyToManyField(Costume, blank=True)
    accessory = models.ManyToManyField(Accessory, blank=True)

    # Handling empty borrowing
    def clean(self):
        # Recursion error
        # if not (self.costume or self.accessory):
            # raise ValidationError('You must specify either accessory or costume for borrowing.')
        # TODO: Check if at least one costume or accessory is present
        # TODO: Check if borrowed_date < return_date
        # Those checks are neccessary for the edit form
        pass

    def __str__(self):
        return 'Borrowing = ' + ' borrowed_date: ' + str(self.borrowed_date) + ' return_date: ' + str(self.return_date) + ' borrowing_expiration: ' + str(self.borrowing_expiration) + ' final_price: ' + str(self.final_price) + ' employee_borrowed: ' + str(self.employee_borrowed) + ' customer: ' + str(self.customer)

