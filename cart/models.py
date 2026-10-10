from django.db import models
from products.models import Product, Customization

# Create your models here.

class Cart(models.Model):
    session_key = models.CharField(
        max_length=100,
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Cart {self.id}"

    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    customization = models.ForeignKey(
        Customization,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='cart_items'
    )

    quantity = models.PositiveIntegerField(
        default=1
    )
    created_at = models.DateTimeField(
    auto_now_add=True
    )
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"