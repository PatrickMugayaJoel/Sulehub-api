# Generated by Django 3.2.16 on 2023-01-14 14:41

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210907_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='DP',
            field=models.CharField(blank=True, max_length=100, verbose_name='Display Picture'),
        ),
        migrations.AddField(
            model_name='user',
            name='DoB',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date of Birth'),
        ),
        migrations.AddField(
            model_name='user',
            name='contact',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='user',
            name='residence',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]