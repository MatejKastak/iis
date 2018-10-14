from django.contrib import admin

from .models import *

admin.site.register(CostumeTemplate)
admin.site.register(Accessory)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Store)
admin.site.register(EmployeeAtStore)
admin.site.register(Manager)
admin.site.register(Costume)
admin.site.register(Borrowing)
admin.site.register(AccessoryToBorrowing)
admin.site.register(CostumeToBorrowing)
admin.site.register(AccessoryToCostumeTemplate)
