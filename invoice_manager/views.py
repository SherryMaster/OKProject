from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from .models import Invoice, Customer, Item


def item_delete(request, pk):
    if request.method == "POST":
        item = Item.objects.get(pk=pk)
        item.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def item_update(request, pk):
    if request.method == "POST":
        item = Item.objects.get(pk=pk)
        item.name = request.POST.get("name")
        item.rate = request.POST.get("rate")
        item.save()
        return JsonResponse({"success": True, "item": {"name": item.name, "rate": item.rate}})

    return JsonResponse({"success": False})

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