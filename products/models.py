from django.db import models

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to = 'categories/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits = 10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Customization(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='customizations'
    )

    color = models.CharField(max_length=50)

    name_to_print = models.CharField(
        max_length=100,
        blank=True
    )

    photo = models.ImageField(
        upload_to='customizations/',
        blank=True,
        null=True
    )

    message = models.TextField(
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.name} - Customization"