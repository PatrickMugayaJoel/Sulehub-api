from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.schools.models import School


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    school = models.ForeignKey(School, to_field='school_id', on_delete=models.CASCADE)
    tags = models.TextField(blank=True)# json.dumps(x) json.loads(self.foo)
    description = models.TextField(blank=True)
    expires_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
