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
    @property
    def subtotal(self):
        return self.product.price * self.quantity
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



class CustomHamper(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="custom_hampers"
    )

    gift_message = models.CharField(
        max_length=250,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Custom Hamper #{self.id}"

    @property
    def total_price(self):
        return sum(
            item.subtotal for item in self.hamper_items.all()
        )


class HamperItem(models.Model):
    hamper = models.ForeignKey(
        CustomHamper,
        on_delete=models.CASCADE,
        related_name="hamper_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=1)

    # Save the price at the time the hamper is created.
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
