from django.db import models
from django.utils import timezone
from apps.users.models import User


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tags = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    image = models.CharField(max_length=100, blank=True)
    _file = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
