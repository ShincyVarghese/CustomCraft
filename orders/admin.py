from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "full_name",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("full_name", "phone", "customer__username")
    readonly_fields = ("created_at",)
    list_editable = ("status",)
    ordering = ("-created_at",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product_name",
        "price",
        "quantity",
    )
