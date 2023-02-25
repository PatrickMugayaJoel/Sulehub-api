from django.db import models
from django.utils import timezone
from users.models import User
from resources.models import Resource


class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    resource = models.ForeignKey(Resource, to_field='id', on_delete=models.CASCADE)
    reference_text = models.CharField(max_length=80, blank=True)
    created_by = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
