from apps.users.models import User
from apps.schools.models import School
from apps.school_extras import (
    Subject, TeacherRegistration,
    StudentRegistration, Level
)


def initial_db():
    ### levels
    level1 = Level(name='Senior One', short_name='S1')
    level2 = Level(name='Senior Two', short_name='S2')
    level3 = Level(name='Senior Three', short_name='S3')
    level4 = Level(name='Senior Four', short_name='S4')
    level1.save()
    level2.save()
    level3.save()
    level4.save()

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
    school1 = School(name='Seeta High', manager=2)
    school2 = School(name='Ntare', manager=2)
    school1.save()
    school2.save()

    ### subjects
    subject1 = Subject(name='Seeta High', manager=2)
    subject2 = Subject(name='Ntare', manager=2)
    subject1.save()
    subject2.save()
