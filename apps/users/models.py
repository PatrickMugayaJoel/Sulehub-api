from django.contrib.auth.models import (
    PermissionsMixin,
    BaseUserManager,
    AbstractBaseUser,
)
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from core.email_service import send_email
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_rest_passwordreset.signals import reset_password_token_created

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_active, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, True, **extra_fields)
        return user

    def get_queryset(self):
        return super(UserManager, self).get_queryset()

    # def get_by_natural_key(self, email):
    #     return self.get(email=email)

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class User(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    ROLES = (
        ('T', 'Teacher'),
        ('S', 'Student'),
        # ('G', 'Guardian'),
        # ('P', 'Publisher'),
    )
    
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=80, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    DoB = models.DateTimeField(_('Date of Birth'), null=True, blank=True)
    contact = PhoneNumberField(blank=True, null=True, unique=True)
    residence = models.CharField(max_length=80, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    country = models.CharField(max_length=30, blank=True)
    Bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=1, choices=ROLES, blank=True)
    DP = models.CharField(_('Display Picture'), max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = AutoDateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        ordering = ['first_name']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.email

    def natural_key(self):
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name, "email":self.email, "contact": self.contact,
            "gender": self.gender, "country": self.country, "residence": self.residence, "DP": self.DP, "Bio": self.Bio
        }

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    first_name = reset_password_token.user.first_name
    if not first_name:
        first_name = "sir/madam"

    send_email(
        template="PASSWORD_RESET",
        TOKEN=reset_password_token.key,
        FIRST_NAME=first_name,
        recipient_list=[reset_password_token.user.email,]
    )
