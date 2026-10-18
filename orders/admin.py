
from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    OrderHamper,
    OrderHamperItem,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product_name",
        "price",
        "quantity",
    )


class OrderHamperItemInline(admin.TabularInline):
    model = OrderHamperItem
    extra = 0
    readonly_fields = (
        "product",
        "product_name",
        "price",
        "quantity",
    )


class OrderHamperInline(admin.TabularInline):
    model = OrderHamper
    extra = 0
    readonly_fields = ("gift_message",)
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "full_name",
        "city",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "city",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "city",
        "pincode",
        "customer__username",
    )

    readonly_fields = ("created_at",)
    list_editable = ("status",)
    ordering = ("-created_at",)
    inlines = [
        OrderItemInline,
        OrderHamperInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product_name",
        "price",
        "quantity",
    )

    list_filter = ("order__status",)
    search_fields = ("product_name",)


@admin.register(OrderHamper)
class OrderHamperAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "gift_message")
    inlines = [OrderHamperItemInline]


@admin.register(OrderHamperItem)
class OrderHamperItemAdmin(admin.ModelAdmin):
    list_display = (
        "hamper",
        "product_name",
        "price",
        "quantity",
    )

    search_fields = ("product_name",)
