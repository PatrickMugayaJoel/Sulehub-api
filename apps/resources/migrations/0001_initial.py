# Generated by Django 4.1.6 on 2023-03-01 19:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=80)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tags', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('image', models.CharField(blank=True, max_length=100)),
                ('_file', models.CharField(blank=True, max_length=100)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
