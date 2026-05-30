from django.db import models
from django.urls import reverse


class Program(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Filière'
        verbose_name_plural = 'Filières'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse('program_list')


class ClassRoom(models.Model):
    name = models.CharField(max_length=120)
    level = models.CharField(max_length=50, help_text='Ex: 1ère année, 2ème année')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='classrooms')

    class Meta:
        ordering = ['program__name', 'level', 'name']
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'
        unique_together = ('name', 'level', 'program')

    def __str__(self):
        return f"{self.name} - {self.level}"

    def get_absolute_url(self):
        return reverse('classroom_list')


class Course(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    credits = models.PositiveSmallIntegerField(default=1)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        ordering = ['title']
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

    def __str__(self):
        return f"{self.title} ({self.code})"

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})

    @property
    def enrolled_students_count(self):
        return self.enrollments.count()


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name='students')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.PROTECT, related_name='students')
    phone_number = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Étudiant'
        verbose_name_plural = 'Étudiants'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class Enrollment(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_DROPPED = 'dropped'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Terminée'),
        (STATUS_DROPPED, 'Abandonnée'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    enrolled_at = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-enrolled_at', 'student__last_name']
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course_enrollment')
        ]

    def __str__(self):
        return f"{self.student} -> {self.course}"

    def get_absolute_url(self):
        return reverse('enrollment_list')
