from django.urls import path
from .views import shop, custom_order


urlpatterns = [

    path(
        '',
        shop,
        name='shop'
    ),
    path(
        'customize/',
        custom_order,
        name='custom_order'
    ),

]