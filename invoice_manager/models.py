from django.db import models
from django.contrib.auth.models import User
import json


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_pending_amount(self):
        amount = 0
        for invoice in self.invoices.all():
            amount += invoice.get_pending_amount()
        return amount

    def __str__(self):
        return self.name


class Invoice(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    amount_paid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.JSONField(default=list) # [{name, rate, quantity}, ...]

    def get_invoice_title(self):
        if self.title:
            return self.title
        return self.customer.name + '\'s invoice No. ' + str(self.pk)

    def get_total_amount(self):
        amount = 0
        for item in self.items:
            amount += item["rate"] * item["quantity"]
        return amount

    def get_total_items(self):
        return len(self.items)

    def get_pending_amount(self):
        return self.get_total_amount() - self.amount_paid

    def add_payment(self, amount):
        if amount > self.get_pending_amount():
            amount -= self.get_pending_amount()
        self.amount_paid += amount
        self.save()
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
