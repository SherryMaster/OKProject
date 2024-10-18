from django.contrib import admin
from .models import Invoice, Customer
# Register your models here.

admin.site.register(Invoice)
admin.site.register(Customer)
