from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class School(models.Model):
    school_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    phone = PhoneNumberField(blank=True, null=True, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    website = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    Bio = models.TextField(blank=True)
    DP = models.CharField(_('Display Picture'), max_length=100, blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(default=timezone.now)
    updated = AutoDateTimeField(default=timezone.now)

    def natural_key(self):
        return {"school_id":self.school_id, "name":self.name, "phone":self.phone, "email":self.email, "website":self.website,
        "country":self.country, "address":self.address, "DP":self.DP, "Bio":self.Bio, "manager":self.manager
    }

    class Meta:
        verbose_name = _('school')
        verbose_name_plural = _('schools')
