from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from users.models import User


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    phone = PhoneNumberField(blank=True, unique=True)
    email = models.EmailField(unique=True)
    website = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    Bio = models.TextField(blank=True)
    DP = models.CharField(_('Display Picture'), max_length=100, blank=True)
    manager = models.ForeignKey(User, to_field='id', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(default=timezone.now)
    updated = AutoDateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('school')
        verbose_name_plural = _('schools')

    def __str__(self):
        return self.email
