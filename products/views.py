
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from products.models import Product
from cart.models import Cart, CustomHamper, HamperItem
from django.db.models import Q


from django.db.models import Q

def shop(request):
    search_query = request.GET.get('q', '').strip()
    print("SEARCH QUERY:", search_query)
    category = request.GET.get('category', '').strip()

    products = Product.objects.select_related('category').all()

    if category:
        products = products.filter(
            category__name__iexact=category
        )

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    return render(request, 'product/shop.html', {
        'products': products,
        'selected_category': category,
        'search_query': search_query,
    })




def custom_order(request):
    return render(request, 'products/custom_order.html')



def customize_hamper(request):
    products = Product.objects.filter(
        stock__gt=0,
        category__name__in=[
            'Gift Hampers',
            'Personalized Gifts',
            'Handmade Gifts',
        ]
    ).exclude(
        name__in=[
            'Self-Care Hamper',
            'Skincare Essentials Hamper',
        ]
    ).order_by('name')

    return render(
        request,
        'customize_hamper.html',
        {'products': products}
    )



def save_hamper(request):
    if request.method != 'POST':
        return redirect('customize_hamper')

    # Read the selected products from the submitted form.
    try:
        selected_items = json.loads(request.POST.get('items', '[]'))
    except (json.JSONDecodeError, TypeError):
        messages.error(request, 'Invalid hamper selections.')
        return redirect('customize_hamper')

    gift_message = request.POST.get('gift_message', '').strip()

    if len(gift_message) > 250:
        messages.error(request, 'Gift message must be 250 characters or fewer.')
        return redirect('customize_hamper')

    if not isinstance(selected_items, list) or not selected_items:
        messages.error(request, 'Please select at least one gift.')
        return redirect('customize_hamper')

    # Validate all products and quantities before saving anything.
    validated_items = []
    seen_ids = set()

    try:
        for item in selected_items:
            if not isinstance(item, dict):
                raise ValueError

            product_id = item.get('id')
            quantity = item.get('quantity')

            if (
                isinstance(product_id, bool)
                or not isinstance(product_id, int)
                or product_id <= 0
                or isinstance(quantity, bool)
                or not isinstance(quantity, int)
                or not 1 <= quantity <= 20
                or product_id in seen_ids
            ):
                raise ValueError

            seen_ids.add(product_id)
            validated_items.append((product_id, quantity))

    except (ValueError, TypeError):
        messages.error(request, 'Please check your selected gifts and quantities.')
        return redirect('customize_hamper')

    product_ids = [product_id for product_id, quantity in validated_items]

    available_products = Product.objects.filter(
        id__in=product_ids,
        stock__gt=0
    )

    product_map = {product.id: product for product in available_products}

    if len(product_map) != len(validated_items):
        messages.error(
            request,
            'One or more selected products are unavailable. Please try again.'
        )
        return redirect('customize_hamper')

    # Ensure Django has a session key before creating the cart.
    if not request.session.session_key:
        request.session.create()

    with transaction.atomic():
        cart, _ = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )

        hamper = CustomHamper.objects.create(
            cart=cart,
            gift_message=gift_message
        )

        for product_id, quantity in validated_items:
            product = product_map[product_id]

            HamperItem.objects.create(
                hamper=hamper,
                product=product,
                quantity=quantity,
                unit_price=product.price
            )

    messages.success(
        request,
        'Your custom hamper has been saved to your cart!'
    )

    return redirect('customize_hamper')
