from django.db import models

# vzor_kostymu
class CostumeTemplate(models.Model):
    # TODO: Rename to name
    costume_type = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return 'CostumeTemplate = ' + ' costume_type: ' + self.costume_type + ' manufacturer: ' + self.manufacturer + ' material: ' + self.material + ' description: ' + self.description

# doplnok
class Accessory(models.Model):
    name = models.CharField(max_length=100)
    manufactured = models.DateField('date created')
    description = models.CharField(max_length=500)

    def __str__(self):
        return 'Accessory = ' + ' name: ' + self.name + ' manufactured: ' + str(self.manufactured) + ' description: ' + self.description

# klient
class Customer(models.Model):
    # TODO: kliets should have logins? Prob uniq
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    # TODO: is CharField the right type for this variable?
    tel_num = models.CharField(max_length=10)

    def __str__(self):
        return 'Customer = ' + ' first_name: ' + self.first_name + ' second_name: ' + self.second_name + ' address: ' + self.address + ' email: ' + self.email + ' tel_num: ' + self.tel_num

# zamestnanec
class Employee(models.Model):
    # TODO: r_cislo as ID?
    login = models.CharField(max_length=100)
    # TODO: check django authentication
    password = models.CharField(max_length=100) # TODO: Too long?
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)

    def __str__(self):
        return 'Employee = ' + ' login: ' + self.login + ' password: ' + self.password + ' first_name: ' + self.first_name + ' second_name: ' + self.second_name

# pobocka
class Store(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return 'Store = ' + ' street: ' + self.street + ' city: ' + self.city

# pracovnik na pobocke
class EmployeeAtStore(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return 'EmployeeAtStore = ' + ' employee_id: ' + str(self.employee_id) + ' store_id: ' + str(self.store_id)

# spravca
class Manager(models.Model): # TODO: Manager, idk if Admin/Administrator would colide with something internal in django?
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    tel_num = models.CharField(max_length=10)

    def __str__(self):
        return 'Manager = ' + ' employee_id: ' + str(self.employee_id) + ' email: ' + self.email + ' tel_num: ' + self.tel_num

# kostym
class Costume(models.Model):
    # TODO: Every costume should have a photo
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100) # TODO: 100 chars?
    manufactured = models.DateField('date created')
    wear_out = models.CharField(max_length=100)
    employee_manage = models.ForeignKey(Employee, on_delete=models.CASCADE)
    costume_template = models.ForeignKey(CostumeTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return 'Costume = ' + ' color: ' + self.color + ' size: ' + self.size + ' manufactured: ' + str(self.manufactured) + ' wear_out: ' + self.wear_out + ' employee_manage: ' + str(self.employee_manage) + ' costume_template: ' + str(self.costume_template)

# vypozicka
class Borrowing(models.Model):
    event = models.CharField(max_length=100)
    borrowed_date = models.DateTimeField('time borrowed')
    return_date = models.DateField('date to return')
    borrowing_expiration = models.DateTimeField('?') # TODO: ?
    final_price = models.IntegerField(default=0)
    employee_borrowed = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return 'Borrowing = ' + ' event: ' + self.event + ' borrowed_date: ' + str(self.borrowed_date) + ' return_date: ' + str(self.return_date) + ' borrowing_expiration: ' + str(self.borrowing_expiration) + ' final_price: ' + self.final_price + ' employee_borrowed: ' + str(self.employee_borrowed) + ' customer: ' + str(self.customer)

# doplnok_vztahuje_sa_k
class AccessoryToBorrowing(models.Model):
    accessory_id = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE)

    def __str__(self):
        return 'AccessoryToBorrowing = ' + ' accessory_id: ' + str(self.accessory_id) + ' borrowing_id: ' + str(self.borrowing_id)

# kostym_vztahuje_sa_k
class CostumeToBorrowing(models.Model):
    costume_id = models.ForeignKey(Costume, on_delete=models.CASCADE)
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE)

    def __str__(self):
        return 'CostumeToBorrowing = ' + ' costume_id: ' + str(self.costume_id) + ' borrowing_id: ' + str(self.borrowing_id)

# patri_k
class AccessoryToCostumeTemplate(models.Model):
    accessory_id = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    costume_template_id = models.ForeignKey(CostumeTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return 'AccessoryToCostumeTemplate = ' + ' accessory_id: ' + str(self.accessory_id) + ' costume_template_id: ' + str(self.costume_template_id)
