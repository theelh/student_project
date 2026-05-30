from datetime import date

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from academics.models import ClassRoom, Course, Enrollment, Program, Student


class Command(BaseCommand):
    help = 'Ajoute des données de démonstration et trois utilisateurs.'

    def handle(self, *args, **options):
        info, _ = Program.objects.get_or_create(name='Génie Informatique', code='GI')
        gestion, _ = Program.objects.get_or_create(name='Gestion', code='GEST')

        gi1, _ = ClassRoom.objects.get_or_create(name='GI1', level='1ère année', program=info)
        gi2, _ = ClassRoom.objects.get_or_create(name='GI2', level='2ème année', program=info)
        ge1, _ = ClassRoom.objects.get_or_create(name='GE1', level='1ère année', program=gestion)

        python_course, _ = Course.objects.get_or_create(title='Python', code='PY101', program=info, defaults={'credits': 4})
        django_course, _ = Course.objects.get_or_create(title='Django', code='DJ201', program=info, defaults={'credits': 5})
        algo_course, _ = Course.objects.get_or_create(title='Algorithmes', code='AL101', program=info, defaults={'credits': 3})
        compta_course, _ = Course.objects.get_or_create(title='Comptabilité', code='CO101', program=gestion, defaults={'credits': 3})

        students = [
            {
                'first_name': 'Salma', 'last_name': 'Alaoui', 'email': 'salma.alaoui@example.com',
                'birth_date': date(2003, 2, 14), 'program': info, 'classroom': gi1,
            },
            {
                'first_name': 'Yassine', 'last_name': 'Bennani', 'email': 'yassine.bennani@example.com',
                'birth_date': date(2002, 11, 3), 'program': info, 'classroom': gi2,
            },
            {
                'first_name': 'Imane', 'last_name': 'Cherkaoui', 'email': 'imane.cherkaoui@example.com',
                'birth_date': date(2004, 1, 28), 'program': gestion, 'classroom': ge1,
            },
        ]

        created_students = []
        for payload in students:
            student, _ = Student.objects.get_or_create(email=payload['email'], defaults=payload)
            created_students.append(student)

        Enrollment.objects.get_or_create(student=created_students[0], course=python_course)
        Enrollment.objects.get_or_create(student=created_students[0], course=django_course)
        Enrollment.objects.get_or_create(student=created_students[1], course=algo_course)
        Enrollment.objects.get_or_create(student=created_students[1], course=django_course)
        Enrollment.objects.get_or_create(student=created_students[2], course=compta_course)

        admin, created = User.objects.get_or_create(username='admin')
        if created:
            admin.is_superuser = True
            admin.is_staff = True
            admin.set_password('Admin12345!')
            admin.save()

        manager, created = User.objects.get_or_create(username='gestionnaire')
        if created:
            manager.set_password('Gestion12345!')
            manager.save()
        manager.groups.set(Group.objects.filter(name='Gestionnaire'))

        viewer, created = User.objects.get_or_create(username='consultation')
        if created:
            viewer.set_password('Consult12345!')
            viewer.save()
        viewer.groups.set(Group.objects.filter(name='Consultation'))

        self.stdout.write(self.style.SUCCESS('Données de démonstration ajoutées.'))
        self.stdout.write('Utilisateurs créés : admin / gestionnaire / consultation')
