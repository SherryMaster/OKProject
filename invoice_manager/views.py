from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from .models import Invoice, Customer, Item


class IndexView(TemplateView):
    template_name = "invoice_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["invoices"] = Invoice.objects.all()
        context["customers"] = Customer.objects.all()
        return context


class ItemsView(CreateView):
    template_name = "invoice_manager/item_list.html"
    model = Item
    fields = ["name", "rate"]
    success_url = "/items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.all()
        return context


class ItemDeleteView(DeleteView):
    model = Item
    success_url = "/items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.all()
        return context