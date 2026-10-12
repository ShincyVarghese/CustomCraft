from django.db import models
from django.contrib.auth.models import User
from products.models import Product


# Create your models here.


class Review(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="product_reviews"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="review_rating_between_1_and_5"
            ),
            models.UniqueConstraint(
                fields=["customer", "product"],
                name="one_review_per_customer_per_product"
            ),
        ]

    def __str__(self):
        return f"{self.customer.username} - {self.product.name} ({self.rating}/5)"
