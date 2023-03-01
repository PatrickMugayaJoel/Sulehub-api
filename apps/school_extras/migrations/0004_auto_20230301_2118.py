from django.db import migrations


def initial_db(apps, schema_editor):
    User = apps.get_model('users', 'User')
    School = apps.get_model('schools', 'School')
    Level = apps.get_model('school_extras', 'Level')
    Subject = apps.get_model('school_extras', 'Subject')
    TeacherRegistration = apps.get_model('school_extras', 'TeacherRegistration')
    StudentRegistration = apps.get_model('school_extras', 'StudentRegistration')


    ### users
    user1 = User(email='mugayajoelpatrick@gmail.com', role='T', password='pbkdf2_sha256$390000$I85twedg82lGW7uXg3lF9c$A6pGRL6xeMdmRYnVyb2wsasV4kUYMHSlhyH3rYdNlik=')
    user2 = User(email='mugayajoelpatrick2@gmail.com', role='T', password='pbkdf2_sha256$390000$I85twedg82lGW7uXg3lF9c$A6pGRL6xeMdmRYnVyb2wsasV4kUYMHSlhyH3rYdNlik=')
    user3 = User(email='jmugaya@nic.co.ug', role='S', password='pbkdf2_sha256$390000$I85twedg82lGW7uXg3lF9c$A6pGRL6xeMdmRYnVyb2wsasV4kUYMHSlhyH3rYdNlik=')
    user4 = User(email='jmugaya2@nic.co.ug', role='S', password='pbkdf2_sha256$390000$I85twedg82lGW7uXg3lF9c$A6pGRL6xeMdmRYnVyb2wsasV4kUYMHSlhyH3rYdNlik=')
    user1.save()
    user2.save()
    user3.save()
    user4.save()

    ### schools
    school1 = School(name='Seeta High', manager=user2)
    school2 = School(name='Ntare', manager=user1)
    school1.save()
    school2.save()

    ### levels
    level1 = Level(name='Senior One', short_name='S1', school=school1)
    level2 = Level(name='Senior Two', short_name='S2', school=school1)
    level3 = school1.level_set.create(name='Senior Three', short_name='S3')
    level4 = school1.level_set.create(name='Senior Four', short_name='S4')
    level1.save()
    level2.save()

    ### subjects
    subject1 = Subject(name='Biology', Level=level1)
    subject2 = Subject(name='Chemistry', Level=level1)
    subject1.save()
    subject2.save()

    subject3 = Subject(name='Physics')
    subject4 = Subject(name='Literature')
    level1.subject_set.add(subject3)
    level1.subject_set.add(subject4)

    ### teacherRegistrations
    tReg1 = TeacherRegistration(teacher=user1, school=school1)
    tReg2 = TeacherRegistration(teacher=user2, school=school1)
    tReg1.save()
    tReg2.save()

    tReg1.subjects.set([subject1, subject2])
    tReg1.subjects.add(subject3, subject4)

    ### StudentRegistration
    sReg1 = StudentRegistration(student=user3, school=school1, level=level1)
    sReg2 = StudentRegistration(student=user4, school=school1, level=level2)
    sReg1.save()
    sReg2.save()

    sReg1.subjects.set(sReg1.level.subject_set.all())
    sReg2.subjects.set(sReg2.level.subject_set.all())


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_initial'),
        ('school_extras', '0003_initial'),
    ]

    operations = [
        migrations.RunPython(initial_db),
    ]
