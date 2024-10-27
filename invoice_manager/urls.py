from django.urls import path
from .views import *


app_name = "invoice_manager"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("items", ItemsView.as_view(), name="items"),
    path("customers", CustomersView.as_view(), name="customers"),
]

ajax_urlpatterns = [
    path("login", login_user, name="login_user"),

    path("items/<int:pk>/delete", item_delete, name="item_delete"),
    path("items/<int:pk>/update", item_update, name="item_update"),
    path("items/create", item_create, name="item_create"),

    path("customers/create", customer_create, name="customer_create"),
    path("customers/<int:pk>/update", customer_update, name="customer_update"),
]

urlpatterns += ajax_urlpatterns
