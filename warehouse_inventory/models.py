from django.db import models
from IMS.products.models import Product

# Create your models here.

class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=255, blank=False, null=False)
    warehouse_location = models.CharField(max_length=255, blank=False, null=False)
    warehouse_capacity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_stocks')
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('warehouse', 'product')
        verbose_name_plural = "Inventories"

    def __str__(self):
        return f"{self.product.name} in {self.warehouse.warehouse_name} - {self.quantity} units"