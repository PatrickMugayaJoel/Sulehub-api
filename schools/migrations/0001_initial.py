# Generated by Django 3.2.16 on 2023-01-17 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import schools.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('school_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=80)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('website', models.CharField(blank=True, max_length=80)),
                ('country', models.CharField(blank=True, max_length=30)),
                ('address', models.CharField(blank=True, max_length=80)),
                ('is_active', models.BooleanField(default=True)),
                ('Bio', models.TextField(blank=True)),
                ('DP', models.CharField(blank=True, max_length=100, verbose_name='Display Picture')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', schools.models.AutoDateTimeField(default=django.utils.timezone.now)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'school',
                'verbose_name_plural': 'schools',
            },
        ),
    ]
