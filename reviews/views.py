
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review, created = Review.objects.get_or_create(
                customer=request.user,
                product=product,
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "comment": form.cleaned_data["comment"],
                },
            )

            if created:
                messages.success(request, "Your review was submitted successfully!")
            else:
                messages.warning(
                    request,
                    "You have already reviewed this product."
                )

            return redirect("product_detail", product_id=product.id)

    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {"form": form, "product": product},
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        customer=request.user
    )

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your review has been updated successfully!"
            )
            return redirect(
                "product_detail",
                product_id=review.product.id
            )
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/add_review.html",
        {
            "form": form,
            "product": review.product,
            "editing": True,
        },
    )

