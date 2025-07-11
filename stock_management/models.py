from django.db import models
from products.models import Products
from warehouse_inventory.models import Warehouse
from user.models import User
from orders.models import PurchaseOrder, SalesOrder
from django.utils import timezone

# Create your models here.

class StockAdjustment(models.Model):
    ADJUSTMENT_TYPE_CHOICES = [
        ('add', 'Add Stock'),
        ('subtract', 'Subtract Stock'),
        ('correction', 'Stock Correction'),
        ('damaged', 'Damaged Goods'),
        ('transfer', 'Stock Transfer'),
        ('lost', 'Loss/Theft'),
        ('returned', 'Returned Stock'),
        ('customer_return', 'Customer Return'),
    ]
    
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='stock_adjustments')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_adjustments')
    adjustment_type = models.CharField(max_length=50, choices=ADJUSTMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    reason = models.TextField(blank=True, null=True)
    adjusted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_adjustments')
    created_at = models.DateTimeField(auto_now_add=True)
    adjustment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.adjustment_type} of {self.quantity} {self.product.name} in {self.warehouse.warehouse_name} on {self.adjustment_date.strftime('%Y-%m-%d')}"
    
class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Shipment'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed_delivery', 'Failed Delivery'),
        ('returned', 'Returned'),
    ]

    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name='shipment', null=True, blank=True)