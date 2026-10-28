from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('profile/edit/',views.profile_edit, name = 'profile_edit'),
    path('shop/',views.shop,name='shop'),
    path('product/<int:product_id>/',views.product_detail,name='product_detail'),
    path('product/<int:product_id>/customize/',views.customize_product,name='customize_product'),
    path('contact/', views.contact, name='contact')
]