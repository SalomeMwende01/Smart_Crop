from django.contrib import admin

from .models import Field, FieldUpdate


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'current_stage', 'assigned_agent', 'planting_date', 'updated_at')
    list_filter = ('current_stage', 'crop_type')
    search_fields = ('name', 'crop_type')


@admin.register(FieldUpdate)
class FieldUpdateAdmin(admin.ModelAdmin):
    list_display = ('field', 'stage', 'created_by', 'created_at')
    list_filter = ('stage',)
    search_fields = ('field__name', 'created_by__username')
