# Generated by Django 4.1.6 on 2023-03-01 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schools', '0001_initial'),
        ('school_extras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherregistration',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
        migrations.AddField(
            model_name='teacherregistration',
            name='subjects',
            field=models.ManyToManyField(to='school_extras.subject'),
        ),
    ]
