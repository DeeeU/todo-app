from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Todo(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, default='')
    completed = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['completed', 'created_at']),
            models.Index(fields=['title', 'completed']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title
