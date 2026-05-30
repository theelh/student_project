from datetime import date

from django.contrib.auth.models import Permission, User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import ClassRoom, Course, Enrollment, Program, Student


class AcademicModelsTest(TestCase):
    def setUp(self):
        self.program = Program.objects.create(name='Informatique', code='INFO')
        self.classroom = ClassRoom.objects.create(name='GI1', level='1ère année', program=self.program)
        self.course = Course.objects.create(title='Python', code='PY101', credits=4, program=self.program)
        self.student = Student.objects.create(
            first_name='Sara',
            last_name='El Idrissi',
            email='sara@example.com',
            birth_date=date(2003, 5, 12),
            program=self.program,
            classroom=self.classroom,
        )

    def test_student_string_representation(self):
        self.assertEqual(str(self.student), 'El Idrissi Sara')

    def test_enrollment_unique_constraint(self):
        Enrollment.objects.create(student=self.student, course=self.course)
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(student=self.student, course=self.course)


class StudentViewsTest(TestCase):
    def setUp(self):
        self.program = Program.objects.create(name='Informatique', code='INFO')
        self.classroom = ClassRoom.objects.create(name='GI1', level='1ère année', program=self.program)
        self.student = Student.objects.create(
            first_name='Youssef',
            last_name='Bennani',
            email='youssef@example.com',
            birth_date=date(2002, 8, 22),
            program=self.program,
            classroom=self.classroom,
        )
        self.user = User.objects.create_user(username='viewer', password='viewer12345')
        view_permission = Permission.objects.get(codename='view_student')
        self.user.user_permissions.add(view_permission)

    def test_student_list_requires_login(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_student_list_authenticated(self):
        self.client.login(username='viewer', password='viewer12345')
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bennani')
