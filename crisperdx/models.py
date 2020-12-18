from django.db import models

# Create your models here.
from task.models import CoreModel


class Setting(CoreModel):
    key = models.CharField(max_length=128, unique=True, verbose_name='键')
    value = models.CharField(max_length=128, verbose_name='值')

    class Meta:
        ordering = ('key',)
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
