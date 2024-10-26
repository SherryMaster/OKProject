from django import forms

from .models import Item, Customer


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("name", "rate")
        labels = {
            "name": "Item Name",
            "rate": "Rate",
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "phone_number")
        labels = {
            "name": "Customer Name",
            "phone_number": "Phone Number",
        }