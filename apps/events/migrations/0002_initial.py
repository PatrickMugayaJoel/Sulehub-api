# Generated by Django 4.1.6 on 2023-03-06 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schools', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
    ]
