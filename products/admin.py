from django.contrib import admin
from .models import Category, Product, Customization



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock",
        "stock_status",
        "created_at",
    )

    list_filter = ("category", "created_at")
    search_fields = ("name", "category__name")
    list_editable = ("price", "stock")
    ordering = ("-created_at",)

    @admin.display(description="Stock Status")
    def stock_status(self, obj):
        if obj.stock > 0:
            return "In Stock"
        return "Out of Stock"


@admin.register(Customization)
class CustomizationAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "product",
        "color",
        "name_to_print",
        "quantity",
        "has_photo",
        "created_at",
    )

    list_filter = ("color", "created_at")
    search_fields = (
        "product__name",
        "name_to_print",
        "message",
    )
    ordering = ("-created_at",)

    @admin.display(description="Photo Uploaded")
    def has_photo(self, obj):
        return bool(obj.photo)
