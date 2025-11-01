from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.
class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'

    class Status(models.TextChoices):
        PENDING = 'PENDING'
        IN_PROGRESS = 'IN_PROGRESS'
        COMPLETED = 'COMPLETED'
        CANCELLED = 'CANCELLED'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_checklist = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    sequence = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title