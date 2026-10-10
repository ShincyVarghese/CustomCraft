from django.contrib import admin
from .models import Category,Product,Customization

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'created_at'
    )

    list_filter = ('category',)

    search_fields = ('name',)


@admin.register(Customization)
class CustomizationAdmin(admin.ModelAdmin):

    list_display = (
        'product',
        'color',
        'name_to_print',
        'quantity',
        'created_at'
    )

    list_filter = (
        'color',
        'created_at'
    )

    search_fields = (
        'product__name',
        'name_to_print',
        'message'
    )