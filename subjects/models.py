from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.models import User
from schools.models import School


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    level = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, to_field='id', null=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, to_field='school_id', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = AutoDateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')

class StudentRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    school = models.ForeignKey(School, to_field='school_id', on_delete=models.CASCADE)
    level = models.CharField(max_length=30)
    academic_year = models.CharField(_(Academic Year), max_length=30, null=True)
    # subjects = models.ManyToManyField(Subject) ## to assign/register subjects
    created = models.DateTimeField(default=timezone.now)
    updated = AutoDateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('academic_year', 'level', 'student')
