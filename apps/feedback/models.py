from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.resources.models import Resource


class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=80, blank=True)
    category = models.CharField(max_length=80, blank=True) # feeds, feedback, review etc
    resource = models.ForeignKey(Resource, to_field='id', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
