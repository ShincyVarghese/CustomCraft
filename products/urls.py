from django.urls import path
from . import views


urlpatterns = [

    path('',views.shop,name='products_shop'),
    path('customize/',views.custom_order,name='custom_order'),
    path('customize-hamper/',views.customize_hamper, name="customize_hamper"),
    path('save-hamper/',views.save_hamper,name="save_hamper"),

]