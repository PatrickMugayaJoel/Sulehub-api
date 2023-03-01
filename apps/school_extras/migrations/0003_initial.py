# Generated by Django 4.1.6 on 2023-03-01 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school_extras', '0002_initial'),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherregistration',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subject',
            name='Level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_extras.level'),
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_extras.level'),
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='subjects',
            field=models.ManyToManyField(to='school_extras.subject'),
        ),
        migrations.AddField(
            model_name='level',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
        migrations.AlterUniqueTogether(
            name='teacherregistration',
            unique_together={('teacher', 'school')},
        ),
        migrations.AlterUniqueTogether(
            name='studentregistration',
            unique_together={('academic_year', 'level', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='level',
            unique_together={('name', 'short_name', 'school')},
        ),
    ]
