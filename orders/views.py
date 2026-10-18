
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.views.decorators.http import require_POST

from .models import Order, OrderItem, OrderHamper, OrderHamperItem
from cart.views import get_cart
from cart.models import CartItem, HamperItem
from products.models import Product
from .forms import CheckoutForm



@login_required
def checkout(request):
    cart = get_cart(request)

    cart_items = list(
        cart.items.select_related("product", "customization").all()
    )

    custom_hampers = list(
        cart.custom_hampers.prefetch_related(
            "hamper_items__product"
        ).all()
    )

    if not cart_items and not custom_hampers:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    product_total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    hamper_total = sum(
        hamper.total_price for hamper in custom_hampers
    )

    total = product_total + hamper_total

    form = CheckoutForm(request.POST or None)

    if request.method == "POST":
        if not form.is_valid():
            messages.error(
                request,
                "Please correct the delivery details."
            )
            return render(request, "orders/checkout.html", {
                "form": form,
                "cart_items": cart_items,
                "custom_hampers": custom_hampers,
                "product_total": product_total,
                "hamper_total": hamper_total,
                "total": total,
            })

        full_name = form.cleaned_data["full_name"]
        phone = form.cleaned_data["phone"]
        address = form.cleaned_data["address"]
        city = form.cleaned_data["city"]
        state = form.cleaned_data["state"]
        pincode = form.cleaned_data["pincode"]

        required_stock = {}

        # Count regular product quantities.
        for item in cart_items:
            if item.quantity < 1:
                messages.error(request, "Invalid product quantity.")
                return redirect("cart")

            required_stock[item.product_id] = (
                required_stock.get(item.product_id, 0)
                + item.quantity
            )

        # Count products inside custom hampers.
        for hamper in custom_hampers:
            for hamper_item in hamper.hamper_items.all():
                if hamper_item.quantity < 1:
                    messages.error(
                        request,
                        "Invalid hamper product quantity."
                    )
                    return redirect("cart")

                required_stock[hamper_item.product_id] = (
                    required_stock.get(hamper_item.product_id, 0)
                    + hamper_item.quantity
                )

        with transaction.atomic():
            locked_products = {}

            # Lock products and verify stock.
            for product_id in sorted(required_stock):
                product = Product.objects.select_for_update().get(
                    pk=product_id
                )
                locked_products[product_id] = product

                if product.stock < required_stock[product_id]:
                    messages.error(
                        request,
                        f"Insufficient stock for {product.name}. "
                        "Please update your cart."
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
                payment_method=form.cleaned_data["payment_method"],
                total_amount=total,
            )

            # Save regular products in the order.
            for item in cart_items:
                product = locked_products[item.product_id]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    customization=item.customization,
                    product_name=product.name,
                    price=product.price,
                    quantity=item.quantity,
                )

            # Save custom hampers and their products.
            for hamper in custom_hampers:
                order_hamper = OrderHamper.objects.create(
                    order=order,
                    gift_message=hamper.gift_message,
                )

                for hamper_item in hamper.hamper_items.all():
                    OrderHamperItem.objects.create(
                        hamper=order_hamper,
                        product=locked_products[hamper_item.product_id],
                        product_name=hamper_item.product.name,
                        price=hamper_item.unit_price,
                        quantity=hamper_item.quantity,
                    )

            # Deduct stock after validating all products.
            for product_id, quantity in required_stock.items():
                product = locked_products[product_id]
                product.stock -= quantity
                product.save(update_fields=["stock"])

            # Clear the cart after saving the order.
            cart.items.all().delete()
            cart.custom_hampers.all().delete()

        messages.success(
            request,
            "Your order has been placed successfully!"
        )
        return redirect("order_success", order_id=order.id)

    return render(request, "orders/checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "custom_hampers": custom_hampers,
        "product_total": product_total,
        "hamper_total": hamper_total,
        "total": total,
    })

@login_required
def my_orders(request):
    orders = (
        Order.objects
        .filter(customer=request.user)
        .prefetch_related("items", "hampers__items")
        .order_by("-created_at")
    )

    return render(
        request,
        "orders/my_orders.html",
        {"orders": orders}
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__customization",
            "hampers__items__product",
        ),
        id=order_id,
        customer=request.user,
    )

    return render(
        request,
        "orders/order_success.html",
        {"order": order},
    )
@login_required
@require_POST
def cancel_order(request, order_id):
    with transaction.atomic():
        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
            customer=request.user,
        )

        if order.status not in ["pending", "confirmed"]:
            messages.error(
                request,
                "This order cannot be cancelled."
            )
            return redirect("my_orders")

        quantities = {}

        # Count regular products.
        for item in order.items.all():
            quantities[item.product_id] = (
                quantities.get(item.product_id, 0)
                + item.quantity
            )

        # Count products inside custom hampers.
        for hamper in order.hampers.all():
            for item in hamper.items.all():
                quantities[item.product_id] = (
                    quantities.get(item.product_id, 0)
                    + item.quantity
                )

        # Restore stock.
        for product_id, quantity in quantities.items():
            Product.objects.filter(id=product_id).update(
                stock=F("stock") + quantity
            )

        order.status = "cancelled"
        order.save(update_fields=["status"])

    messages.success(
        request,
        f"Order #{order.id} has been cancelled successfully."
    )
    return redirect("my_orders")