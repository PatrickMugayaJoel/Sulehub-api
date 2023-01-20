from django.db import models
from django.utils import timezone
from users.models import User
from schools.models import School


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    school = models.ForeignKey(School, to_field='school_id', on_delete=models.CASCADE)
    tags = models.TextField(blank=True)# json.dumps(x) json.loads(self.foo)
    description = models.TextField(blank=True)
    expires_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)