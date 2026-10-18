
from .views import get_cart


def cart_item_count(request):
    if not request.session.session_key:
        return {"cart_item_count": 0}

    cart = get_cart(request)

    regular_count = sum(
        item.quantity for item in cart.items.all()
    )

    hamper_count = sum(
        item.quantity
        for hamper in cart.custom_hampers.all()
        for item in hamper.hamper_items.all()
    )

    return {
        "cart_item_count": regular_count + hamper_count
    }
