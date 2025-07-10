from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Products(models.Model):
    name = models.CharField(max_length = 100, null = False)
    description = models.TextField(blank = True, null = True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'products')
    cost_price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    selling_price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.00)
    low_stock_threshold = models.IntegerField(default = 10, help_text = "Minimum quantity before low stock alert")
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
    @property
    def total_quantity_in_stock(self):
        return self.inventory_stocks.aggregate(total = models.Sum('quantity'))['total'] or 0