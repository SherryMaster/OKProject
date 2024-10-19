from django.urls import path
from .views import *


app_name = "invoice_manager"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("items", ItemsView.as_view(), name="items"),
    path("items/<int:pk>/delete", ItemDeleteView.as_view(), name="item_delete"),
]
