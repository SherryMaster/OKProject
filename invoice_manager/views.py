from django.db import IntegrityError
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView
from .models import Invoice, Customer, Item


def item_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        rate = request.POST.get("rate")
        try:
            item = Item()
            item.name = name
            item.rate = rate
            item.save()
            return JsonResponse({"success": True, "item": {"pk": item.pk, "name": item.name, "rate": item.rate}, "reason": "Item created successfully"})
        except IntegrityError as e:
            return JsonResponse({"success": False, "reason": f"Item with name \"{name}\" already exists"})

    return JsonResponse({"success": False, "reason": "Invalid request"})


def item_delete(request, pk):
    print(pk)
    if request.method == "POST":
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False})

    return JsonResponse({"success": False})


def item_update(request, pk):
    if request.method == "POST":
        name = request.POST.get("name")
        rate = request.POST.get("rate")
        item = Item.objects.get(pk=pk)
        item.name = name
        item.rate = rate
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


class ItemsView(ListView):
    template_name = "invoice_manager/item_list.html"
    model = Item
    context_object_name = "items"
