from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Invoice(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    amount = models.FloatField()
    amount_paid = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.name + ' - ' + str(self.amount_paid) + '/' + str(self.amount)


class Customer(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
