from datetime import date

from django.conf import settings
from django.db import models


class FieldStage(models.TextChoices):
    PLANTED = 'PLANTED', 'Planted'
    GROWING = 'GROWING', 'Growing'
    READY = 'READY', 'Ready'
    HARVESTED = 'HARVESTED', 'Harvested'


class FieldStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    AT_RISK = 'AT_RISK', 'At Risk'
    COMPLETED = 'COMPLETED', 'Completed'


class Field(models.Model):
    name = models.CharField(max_length=200)
    crop_type = models.CharField(max_length=100)
    planting_date = models.DateField()
    current_stage = models.CharField(max_length=16, choices=FieldStage.choices, default=FieldStage.PLANTED)
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_fields',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_fields',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.name} ({self.crop_type})'

    @property
    def computed_status(self):
        if self.current_stage == FieldStage.HARVESTED:
            return FieldStatus.COMPLETED

        today = date.today()
        days_since_planting = max((today - self.planting_date).days, 0)

        risk_thresholds = {
            FieldStage.PLANTED: 14,
            FieldStage.GROWING: 45,
            FieldStage.READY: 20,
        }

        threshold = risk_thresholds.get(self.current_stage)
        if threshold is not None and days_since_planting > threshold:
            return FieldStatus.AT_RISK

        return FieldStatus.ACTIVE


class FieldUpdate(models.Model):
    field = models.ForeignKey(Field, related_name='updates', on_delete=models.CASCADE)
    stage = models.CharField(max_length=16, choices=FieldStage.choices)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='field_updates', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Update for {self.field.name} at {self.created_at:%Y-%m-%d %H:%M}'
