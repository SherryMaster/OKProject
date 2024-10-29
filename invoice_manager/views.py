from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView, DetailView
from .models import Invoice, Customer, Item

import json


def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


# region Item Methods
@login_required
def item_create(request):
    if request.method == "POST":
        if not (request.user.profile.is_employee and request.user.is_superuser):
            return JsonResponse({"success": False, "reason": "Only employees and admins can create items"})
        name = request.POST.get("name")
        rate = request.POST.get("rate")
        try:
            item = Item()
            item.name = name
            item.rate = rate
            item.save()
            return JsonResponse({"success": True, "item": {"pk": item.pk, "name": item.name, "rate": item.rate},
                                 "reason": "Item created successfully"})
        except IntegrityError as e:
            return JsonResponse({"success": False, "reason": f"Item with name \"{name}\" already exists"})

    return JsonResponse({"success": False, "reason": "Invalid request"})


@login_required
def item_delete(request, pk):
    print(pk)
    if request.method == "POST":
        if not (request.user.profile.is_employee and request.user.is_superuser):
            return JsonResponse({"success": False, "reason": "Only employees and admins can delete items"})
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return JsonResponse({"success": True, "reason": "Item deleted successfully"})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "reason": "Item not found"})

    return JsonResponse({"success": False, "reason": "Invalid request"})


@login_required
def item_update(request, pk):
    if request.method == "POST":
        if not (request.user.profile.is_employee and request.user.is_superuser):
            return JsonResponse({"success": False, "reason": "Only employees and admins can update items"})
        name = request.POST.get("name")
        rate = request.POST.get("rate")
        item = Item.objects.get(pk=pk)
        item.name = name
        item.rate = rate
        item.save()
        return JsonResponse(
            {"success": True, "item": {"name": item.name, "rate": item.rate}, "reason": "Item updated successfully"})

    return JsonResponse({"success": False, "reason": "Invalid request"})


# endregion

# region Customer Methods

@login_required
def customer_create(request):
    if request.method == "POST":
        if not (request.user.profile.is_employee and request.user.is_superuser):
            return JsonResponse({"success": False, "reason": "Only employees and admins can create customers"})
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        try:
            customer = Customer()
            customer.name = name
            customer.phone_number = phone_number
            customer.address = address
            customer.save()
            return JsonResponse({"success": True, "customer": {"pk": customer.pk, "name": customer.name,
                                                               "phone_number": customer.phone_number,
                                                               "address": customer.address,
                                                               "pending_amount": customer.get_pending_amount()},
                                 "reason": "Customer created successfully"})
        except IntegrityError as e:
            return JsonResponse({"success": False, "reason": f"Customer with name \"{name}\" already exists"})

    return JsonResponse({"success": False, "reason": "Invalid request"})


@login_required
def customer_update(request, pk):
    if request.method == "POST":
        if not (request.user.profile.is_employee and request.user.is_superuser):
            return JsonResponse({"success": False, "reason": "Only employees and admins can update customers"})
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        customer = Customer.objects.get(pk=pk)
        customer.name = name
        customer.phone_number = ''.join(c for c in phone_number if c.isdigit())
        customer.address = address
        customer.save()
        return JsonResponse({"success": True, "customer": {"name": customer.name, "phone_number": customer.phone_number,
                                                           "address": customer.address,
                                                           "pending_amount": customer.get_pending_amount()},
                             "reason": "Customer updated successfully"})

    return JsonResponse({"success": False, "reason": "Invalid request"})


# endregion

# region Invoice Methods
@login_required
def invoice_create(request):
    if request.method == "POST":

        if not (request.user.profile.is_employee and request.user.is_superuser):
            return JsonResponse({"success": False, "reason": "Only employees and admins can create invoices"})

        data = json.loads(request.body)

        title = data["title"]
        customer_pk = data["customer"]
        items = data["items"]
        names = items["name"]
        rates = items["rate"]
        quantities = items["quantity"]

        try:
            customer = Customer.objects.get(pk=customer_pk)
        except Exception as e:
            return JsonResponse({"success": False, "reason": f"Customer with pk \"{customer_pk}\" not found"})

        try:
            invoice = Invoice()
            invoice.title = title or f"{customer}'s Invoice No. {invoice.pk}"
            invoice.customer = customer
            invoice.created_by = request.user
            invoice.make_item_list(names, rates, quantities)
            invoice.save()
            return JsonResponse({"success": True, "invoice": {"pk": invoice.pk, "title": invoice.get_invoice_title(),
                                                              "amount_paid": invoice.amount_paid,
                                                              "total_amount": invoice.get_total_amount(),
                                                              "pending_amount": invoice.get_pending_amount(),
                                                              "items": invoice.items},
                                 "reason": "Invoice created successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "reason": f"{e}"})

    return JsonResponse({"success": False, "reason": "Invalid request"})

# endregion


class IndexView(TemplateView):
    template_name = "invoice_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["invoices"] = Invoice.objects.filter(created_at__gte=timezone.now() - timedelta(days=1)).order_by("-id")
        context["customers"] = Customer.objects.filter(created_at__gte=timezone.now() - timedelta(days=1)).order_by(
            "-id")
        return context


class ItemsView(ListView):
    template_name = "invoice_manager/item_list.html"
    model = Item
    context_object_name = "items"


class CustomersView(ListView):
    template_name = "invoice_manager/customer_list.html"
    model = Customer
    context_object_name = "customers"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["pending_amounts"] = Customer.objects.all().annotate(pending_amount=Sum("invoices__amount") - Sum("invoices__amount_paid"))
    #     return context


class CustomerDetailView(DetailView):
    template_name = "invoice_manager/customer_detail.html"
    model = Customer
    context_object_name = "customer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoices = Invoice.objects.filter(customer=self.object)
        context["invoices"] = Invoice.objects.filter(customer=self.object).order_by("-id")
        return context


class InvoiceListView(ListView):
    template_name = "invoice_manager/invoice_list.html"
    model = Invoice
    context_object_name = "invoices"
    ordering = "-id"


class CreateInvoiceView(TemplateView):
    template_name = "invoice_manager/invoice_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customers"] = Customer.objects.all()
        context["items"] = Item.objects.all()
        return context


class InvoiceDetailView(DetailView):
    template_name = "invoice_manager/invoice_detail.html"
    model = Invoice
    context_object_name = "invoice"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.items
        for item in items:
            item["total"] = int(item["rate"]) * int(item["quantity"])
        context["items"] = self.object.items
        return context
