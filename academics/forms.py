from django import forms

from .models import ClassRoom, Course, Enrollment, Program, Student


class DateInput(forms.DateInput):
    input_type = 'date'


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'code', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'level', 'program']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'description', 'credits', 'program']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'program',
            'classroom',
            'phone_number',
        ]
        widgets = {
            'birth_date': DateInput(),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 3})}
