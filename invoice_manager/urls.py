from django.urls import path
from .views import *


app_name = "invoice_manager"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("items", ItemsView.as_view(), name="items"),
    path("items/<int:pk>/delete", item_delete, name="item_delete"),
    path("items/<int:pk>/update", item_update, name="item_update"),
]
