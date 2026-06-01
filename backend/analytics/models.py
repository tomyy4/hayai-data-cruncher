from django.db import models

from django.db import models

class Store(models.Model):
    """Represents a store inside our multi-tentant platform"""
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, db_index=True) # Indexed for fast searchers
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Products associated to specific store."""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_lines')
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(db_index=True) # Indexed to work with dynamic filters

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"