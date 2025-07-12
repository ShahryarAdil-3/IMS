from django.db import models
from user.models import User

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Role(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class Employee(models.Model):
    user_account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='employees')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    hire_date = models.DateField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_account.username} ({self.role.title if self.role else 'No Role'}) - {self.department.name if self.department else 'No Department'}"
    
class Salary(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('overdue', 'Overdue'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    month = models.CharField(max_length=20, null=False, blank=False)
    year = models.PositiveIntegerField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_on = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Salaries'
        unique_together = ('employee', 'month', 'year')

    def __str__(self):
         return f"Salary for {self.employee} - {self.month} {self.year}: {self.amount} ({self.status})"

class LeaveRequest(models.Model):
    TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('earned', 'Earned Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=False, blank=False)
    from_date = models.DateField(null=False, blank=False)
    to_date = models.DateField(null=False, blank=False)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    approved_on = models.DateTimeField(null=True, blank=True)
    rejected_on = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='leave_requests_reviewed')
    review_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Leave request for {self.employee} from {self.from_date} to {self.to_date} ({self.status})"