from django.db import models
from django.utils import timezone
from users.models import User
from resources.models import Resource


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, blank=True)
    category = models.CharField(max_length=80, blank=True) # feeds, feedback, review etc
    resource = models.ForeignKey(Resource, to_field='id', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
