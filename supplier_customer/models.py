from django.db import models

# Create your models here.

class Supplier(models.Model):
    supplier_company_name = models.CharField(max_length=255, blank=False, null=False)
    supplier_name = models.CharField(max_length=255, blank=False, null=False)
    supplier_email = models.EmailField()
    supplier_phone_number = models.CharField(max_length=20, blank=False, null=False)
    supplier_address = models.TextField(blank=False, null=False)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.supplier_company_name

class Customer(models.Model):
    customer_company_name = models.CharField(max_length=255, blank=False, null=False)
    customer_name = models.CharField(max_length=255, blank=False, null=False)
    customer_email = models.EmailField()
    customer_phone_number = models.CharField(max_length=20, blank=False, null=False)
    customer_address = models.TextField(blank=False, null=False)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_company_name
    
    def get_total_orders(self):
        return self.order_set.count()
    def get_total_spent(self):
        return sum(order.get_total_amount() for order in self.sales_orders.filter(status='delivered'))