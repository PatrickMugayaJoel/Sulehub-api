# Generated by Django 3.2.16 on 2023-01-19 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=80)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tags', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.CharField(blank=True, max_length=100)),
                ('_file', models.CharField(blank=True, max_length=100)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
