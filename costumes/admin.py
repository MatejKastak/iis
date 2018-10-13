from django.contrib import admin

# from .models import * ??
from .models import CostumeTemplate, Accessory, Customer

admin.site.register(CostumeTemplate)
admin.site.register(Accessory)
admin.site.register(Customer)
