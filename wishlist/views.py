from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Wishlist, WishlistItem
# Create your views here.





@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(
        customer=request.user
    )

    items = wishlist.items.select_related(
        "product",
        "product__category"
    ).all()

    return render(
        request,
        "wishlist/wishlist.html",
        {"wishlist": wishlist, "items": items}
    )


@login_required
@require_POST
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(
        customer=request.user
    )

    WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )

    return redirect("wishlist")


@login_required
@require_POST
def remove_from_wishlist(request, item_id):
    wishlist, created = Wishlist.objects.get_or_create(
        customer=request.user
    )

    item = get_object_or_404(
        WishlistItem,
        id=item_id,
        wishlist=wishlist
    )

    item.delete()

    return redirect("wishlist")
