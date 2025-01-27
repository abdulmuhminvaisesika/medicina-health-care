from django.db import models

# Create your models here.

class Order(models.Model):
    order_status_choices = [
        ('cart_stage', 'Cart Stage'),
        ('Processing', 'Processing'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    owner = models.ForeignKey(
        'user_app.CustomUser',
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,  # Allow null values when the user is deleted
        blank=True  # Allow this field to be optional in forms
    )
    order_status = models.CharField(max_length=20, choices=order_status_choices, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.order_status}"


class OrderItem(models.Model):
    product = models.ForeignKey(
        'product_app.Product',
        on_delete=models.SET_NULL,
        related_name='added_carts',
        null=True,  # Allow null values when the product is deleted
        blank=True  # Allow this field to be optional in forms
    )
    quantity = models.PositiveIntegerField(default=1)
    owner = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OrderItem #{self.id} for Order #{self.owner.id}"
