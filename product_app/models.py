from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    MRP = models.DecimalField(max_digits=10, decimal_places=2)
    GST = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField()
    description = models.TextField()
    is_stock = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    product_category = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.title}"
