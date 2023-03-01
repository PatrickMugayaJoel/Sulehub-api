from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.schools.models import School


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

## Levels
#############################################
class LevelManager(models.Manager):
    def get_by_natural_key(self, id):
        return self.get(id=id)

class Level(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    short_name = models.CharField(max_length=5, blank=True)
    school = models.ForeignKey(School, to_field='school_id', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    objects = LevelManager()

    class Meta:
        unique_together = ('name', 'short_name', 'school',)

## Subjects
#############################################
class SubjectManager(models.Manager):
    def get_by_natural_key(self, id):
        return self.get(id=id)

class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    Level = models.ForeignKey(Level, on_delete=models.CASCADE)

    objects = SubjectManager()

## Teachers
#############################################
class TeacherRegistration(models.Model):
    reg_id = models.BigAutoField(primary_key=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE) # TODO: show more than an id
    school = models.ForeignKey(School, to_field='school_id', on_delete=models.CASCADE) # TODO: show more than an id
    subjects = models.ManyToManyField(Subject)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('teacher', 'school',)

## Students
#############################################
class StudentRegistration(models.Model):
    reg_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE) # TODO: show more than an id
    school = models.ForeignKey(School, to_field='school_id', on_delete=models.CASCADE) # TODO: show more than an id
    level = models.ForeignKey(Level, null=True, on_delete=models.SET_NULL)
    academic_year = models.CharField(_("Academic Year"), max_length=30, null=True)
    subjects = models.ManyToManyField(Subject)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = AutoDateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('academic_year', 'level', 'student')
