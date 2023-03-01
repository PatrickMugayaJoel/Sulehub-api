from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.resources.models import Resource


class Sale(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    resource = models.ForeignKey(Resource, to_field='id', on_delete=models.CASCADE)
    reference_text = models.CharField(max_length=80, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
