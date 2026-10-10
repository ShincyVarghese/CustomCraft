from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from products.models import Product

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

def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('product_detail', product_id=product_id)

    product = get_object_or_404(Product, id=product_id)

    cart = get_cart(request)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if quantity > product.stock:
        return render(
            request,
            'product_detail.html',
            {
                'product': product,
                'error': 'Requested quantity exceeds available stock.'
            }
        )

    cart_item = CartItem.objects.filter(
        cart=cart,
        product=product,
        customization__isnull=True
    ).first()

    if cart_item:
        if cart_item.quantity + quantity > product.stock:
            return render(
                request,
                'product_detail.html',
                {
                    'product': product,
                    'error': 'Requested quantity exceeds available stock.'
                }
            )

        cart_item.quantity += quantity
        cart_item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    return redirect('cart')


def cart_view(request):

    cart = get_cart(request)

    cart_items = cart.items.select_related('product').all()

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'cart.html',
        {
            'cart': cart,
            'cart_items': cart_items,
            'total': total,
        }
    )

def update_cart(request, item_id):

    cart = get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()

    else:
        cart_item.delete()

    return redirect('cart')


def remove_from_cart(request, item_id):

    cart = get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    cart_item.delete()

    return redirect('cart')