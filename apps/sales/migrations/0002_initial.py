# Generated by Django 4.1.6 on 2023-03-06 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0001_initial'),
        ('resources', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sale',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.resource'),
        ),
    ]
