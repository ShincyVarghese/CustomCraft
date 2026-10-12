
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem
from cart.views import get_cart
from .models import Order
from django.views.decorators.http import require_POST


@login_required
def checkout(request):
    cart = get_cart(request)

    cart_items = list(
        cart.items.select_related("product", "customization").all()
    )

    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        pincode = request.POST.get("pincode", "").strip()

        if not all([full_name, phone, address, city, state, pincode]):
            messages.error(request, "Please complete all delivery details.")
            return render(request, "orders/checkout.html", {
                "cart_items": cart_items,
                "total": total,
            })

        with transaction.atomic():
            # Lock product rows and check stock before placing the order.
            for item in cart_items:
                product = item.product.__class__.objects.select_for_update().get(
                    pk=item.product_id
                )
                if item.quantity < 1 or item.quantity > product.stock:
                    messages.error(
                        request,
                        f"Insufficient stock for {product.name}.",
                    )
                    return redirect("cart")

            order = Order.objects.create(
                customer=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                payment_method="cod",
                total_amount=total,
            )

            for item in cart_items:
                product = item.product.__class__.objects.select_for_update().get(
                    pk=item.product_id
                )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    customization=getattr(item, "customization", None),
                    product_name=product.name,
                    price=product.price,
                    quantity=item.quantity,
                )

                product.stock -= item.quantity
                product.save(update_fields=["stock"])

            cart.items.all().delete()

        return redirect("order_success", order_id=order.id)

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total": total,
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        id=order_id,
        customer=request.user,
    )

    return render(request, "orders/order_success.html", {
        "order": order,
    })


@login_required
def my_orders(request):
    orders_list = Order.objects.filter(
        customer=request.user
    ).order_by("-created_at")

    print("Logged-in user:", request.user.username)
    print("Orders found:", orders_list.count())

    return render(request, "orders/my_orders.html", {
        "orders": orders_list,
    })
@login_required
@require_POST
def cancel_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user,
    )

    if order.status in ["pending", "confirmed"]:
        order.status = "cancelled"
        order.save(update_fields=["status"])

        messages.success(
            request,
            f"Order #{order.id} has been cancelled successfully."
        )
    else:
        messages.error(
            request,
            "This order cannot be cancelled because it has already been shipped, delivered, or cancelled."
        )

    return redirect("my_orders")