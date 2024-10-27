from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_pending_amount(self):
        amount = 0
        for invoice in self.invoices.all():
            amount += invoice.amount - invoice.amount_paid
        return amount

    def __str__(self):
        return self.name


class Invoice(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    amount = models.IntegerField()
    amount_paid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.JSONField(default=list)

    def __str__(self):
        return self.title or self.customer.name + '\'s invoice with amount ' + str(self.amount_paid) + '/' + str(self.amount)


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rate = models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    is_employee = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
