from django.db import models
from django.utils import timezone

class Todo(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True, null=True)
  completed = models.BooleanField(default=False)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return self.title
