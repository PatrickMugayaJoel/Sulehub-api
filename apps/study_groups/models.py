from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.schools.models import School


class StudyGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    school = models.ForeignKey(School, to_field='school_id', on_delete=models.CASCADE)
    level = models.CharField(max_length=80, blank=True)
    tags = models.TextField(blank=True)# json.dumps(x) json.loads(self.foo)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

class GroupRegistration(models.Model):
    member_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE) # TODO: show more than an id
    study_group = models.ForeignKey(StudyGroup, to_field='id', on_delete=models.CASCADE) # TODO: show more than an id
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'study_group',)
