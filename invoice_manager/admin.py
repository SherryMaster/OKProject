from django.contrib import admin
from .models import Invoice, Customer, Item, Profile
# Register your models here.

admin.site.register(Invoice)
admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(Profile)
