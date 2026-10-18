from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from products.models import Product
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.

def get_cart(request):
    """
    Get the current customer's cart.
    """

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(
        session_key=session_key
    )

    return cart


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect('product_detail', product_id=product_id)

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect('product_detail', product_id=product_id)

    if product.stock <= 0:
        messages.error(request, "Sorry, this product is out of stock.")
        return redirect('product_detail', product_id=product_id)

    cart = get_cart(request)

    cart_item = CartItem.objects.filter(
        cart=cart,
        product=product,
        customization__isnull=True
    ).first()

    current_quantity = cart_item.quantity if cart_item else 0

    if current_quantity + quantity > product.stock:
        messages.error(
            request,
            f"Only {product.stock - current_quantity} more item(s) can be added."
        )
        return redirect('product_detail', product_id=product_id)

    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    messages.success(request, "Product added to your cart.")
    return redirect('cart')


def cart_view(request):
    cart = get_cart(request)

    # Retrieve regular product cart items.
    cart_items = cart.items.select_related(
        'product',
        'customization'
    ).all()

    # Retrieve custom hampers and their selected products.
    custom_hampers = cart.custom_hampers.prefetch_related(
        'hamper_items__product'
    ).all()

    # Calculate the regular product total.
    product_total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    # Calculate the custom hamper total.
    hamper_total = sum(
        hamper.total_price
        for hamper in custom_hampers
    )

    # Calculate the combined cart total.
    total = product_total + hamper_total

    return render(
        request,
        'cart.html',
        {
            'cart': cart,
            'cart_items': cart_items,
            'custom_hampers': custom_hampers,
            'product_total': product_total,
            'hamper_total': hamper_total,
            'total': total,
        }
    )


@require_POST
def update_cart(request, item_id):
    cart = get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect('cart')

    if quantity <= 0:
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")

    elif quantity > cart_item.product.stock:
        messages.error(
            request,
            f"Only {cart_item.product.stock} items are available."
        )

    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart quantity updated.")

    return redirect('cart')




@require_POST
def remove_from_cart(request, item_id):
    
    cart = get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    cart_item.delete()
    messages.success(request, "Item removed from your cart.")

    return redirect('cart')
