
from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_orders, name="orders"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("cancel/<int:order_id>",views.cancel_order,name="cancel_order"),
]
