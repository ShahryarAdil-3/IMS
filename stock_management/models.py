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

    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name='shipment')
    shipped_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments_processed')
    shipment_date = models.DateTimeField(null=False, blank=False)
    carrier = models.CharField(max_length=100, blank=False, null=False)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment for SO #{self.sales_order.id} - Status: {self.status}"

class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('online_payment', 'Online Payment'),
    ]
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments_received')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"payment of {self.amount} for SO #{self.sales_order.id} on {self.payment_method}"