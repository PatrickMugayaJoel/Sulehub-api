from django.db import migrations
from django.conf import settings


def initial_db(apps, schema_editor):
    User = apps.get_model('users', 'User')
    School = apps.get_model('schools', 'School')
    Invitation = apps.get_model('events', 'Invitation')
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
    subject1 = Subject(name='Biology', level=level1)
    subject2 = Subject(name='Chemistry', level=level1)
    subject3 = Subject(name='Physics', level=level1)
    subject4 = Subject(name='Literature', level=level1)
    subject1.save()
    subject2.save()
    subject3.save()
    subject4.save()

    ### teacherRegistrations
    tReg1 = TeacherRegistration(teacher=user1, school=school1)
    tReg2 = TeacherRegistration(teacher=user2, school=school1)
    tReg1.save()
    tReg2.save()

    tReg1.subjects.set([subject1, subject2])
    tReg1.subjects.add(subject3, subject4)

    ### invitations
    invite1 = Invitation(email='mugayajoelpatrick@gmail.com', user_type='teacher', school=school2)
    invite2 = Invitation(email='jmugaya@nic.co.ug', user_type='student', school=school2)
    invite1.save()
    invite2.save()

    ### StudentRegistration
    sReg1 = StudentRegistration(student=user3, school=school1, level=level1)
    sReg2 = StudentRegistration(student=user4, school=school1, level=level2)
    sReg1.save()
    sReg2.save()

    sReg1.subjects.set(sReg1.level.subject_set.all())
    sReg2.subjects.set(sReg2.level.subject_set.all())

    ### Study Groups
    StudyGroup = apps.get_model('study_groups', 'StudyGroup')
    sGrp1 = StudyGroup(name="Physics Study Group 1", level=level1, created_by=user3)
    sGrp2 = StudyGroup(name="Literature Study Group 2", level=level1, created_by=user4)
    sGrp1.save()
    sGrp2.save()

    ### Study Group Registrations
    sGrpRegistration = apps.get_model('study_groups', 'GroupRegistration')
    sGrpReg1 = sGrpRegistration(student=user3, study_group=sGrp1)
    sGrpReg1.save()

    ### Events
    Event = apps.get_model('events', 'Event')
    events1 = Event(name="Talent Show", school=school1, created_by=user4)
    events2 = Event(name="Charity", school=school1, created_by=user3)
    events3 = Event(name="Sports Gala", school=school1, created_by=user3)
    events4 = Event(name="Visitation Day", school=school1, created_by=user3)
    events1.save()
    events2.save()
    events3.save()
    events4.save()

    ### resources
    Resource = apps.get_model('resources', 'Resource')
    resource1 = Resource(name="Introduction to Biology", price=85000.00, created_by=user1)
    resource2 = Resource(name="Physics Fundamentals vol-1", price=76000.00, created_by=user1)
    resource1.save()
    resource2.save()

    ### feedback
    Feedback = apps.get_model('feedback', 'Feedback')
    feedback1 = Feedback(title="Tortor at rhoncus tempor condimentum", resource=resource1, created_by=user3)
    feedback2 = Feedback(title="Morbi sit pharetra senectus praesent", resource=resource1, created_by=user4)
    feedback1.save()
    feedback2.save()

    ### sales
    Sale = apps.get_model('sales', 'Sale')
    sale1 = Sale(price=84000.00, resource=resource1, created_by=user3)
    sale2 = Sale(price=86000.00, resource=resource1, created_by=user4)
    sale1.save()
    sale2.save()


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_initial'),
        ('school_extras', '0003_initial'),
        ('events', '0003_initial'),
        ('feedback', '0002_initial'),
        ('resources', '0002_initial'),
        ('sales', '0002_initial'),
        ('study_groups', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(initial_db),
    ]
