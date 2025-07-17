from django.db import models
from user.models import User

# Create your models here.

class ActivityLog(models.Mode):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    target_table = models.CharField(max_length=255)
    target_id = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.user or 'System'} - {self.action}"

class AuditLog(models.Model):
    table_name = models.CharField(max_length=100)
    record_id = models.IntegerField()
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    change_summary = models.TextField() # Could be JSONField for structured diffs
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit: {self.table_name} ID {self.record_id} changed by {self.changed_by or 'System'} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.URLField(blank=True, null=True) # Optional link to relevant page
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}: {self.message[:50]}..."