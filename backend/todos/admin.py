from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
  list_display = ('title', 'completed', 'created_at', 'updated_at')
  list_filter = ('completed', 'created_at')
  search_fields = ('title', 'description')
  list_editable = ('completed',)
  fields = ('title', 'description', 'completed')
  readonly_fields = ('created_at', 'updated_at')

# Register your models here.
