from django.db import models
from supplier_customer.models import Customer
from user.models import User
from django.utils import timezone
# Create your models here.

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_received', 'Partially Received'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='purchase_orders', null=True)
    order_date = models.DateTimeField(default=timezone.now)
    expected_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='purchase_orders_created') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO #{self.id} from {self.customer.name if self.customer else 'Unknown'} on {self.order_date.strftime('%Y-%m-%d')}"
    
    def get_total_cost(self):
        return sum(item.total_price for item in self.items.all())