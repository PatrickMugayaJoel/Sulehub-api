# Generated by Django 4.1.6 on 2023-03-09 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_extras', '0005_alter_studentregistration_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentregistration',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='school_extras.subject'),
        ),
        migrations.AlterField(
            model_name='teacherregistration',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='school_extras.subject'),
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together={('name', 'level')},
        ),
    ]
