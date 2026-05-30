from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ClassRoomForm, CourseForm, EnrollmentForm, ProgramForm, StudentForm
from .models import ClassRoom, Course, Enrollment, Program, Student


class DeleteMessageMixin:
    delete_success_message = 'Suppression effectuée avec succès.'

    def form_valid(self, form):
        messages.success(self.request, self.delete_success_message)
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'academics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counts'] = {
            'students': Student.objects.count(),
            'courses': Course.objects.count(),
            'enrollments': Enrollment.objects.count(),
            'programs': Program.objects.count(),
            'classrooms': ClassRoom.objects.count(),
        }
        context['recent_enrollments'] = Enrollment.objects.select_related('student', 'course')[:8]
        context['students_by_program'] = Program.objects.annotate(total=Count('students')).order_by('-total', 'name')
        return context


class ProgramListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Program
    permission_required = 'academics.view_program'
    template_name = 'academics/program_list.html'
    context_object_name = 'programs'

class ProgramCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Program
    form_class = ProgramForm
    permission_required = 'academics.add_program'
    template_name = 'academics/program_form.html'
    success_url = reverse_lazy('program_list')
    success_message = 'Filière ajoutée avec succès.'

class ProgramUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Program
    form_class = ProgramForm
    permission_required = 'academics.change_program'
    template_name = 'academics/program_form.html'
    success_url = reverse_lazy('program_list')
    success_message = 'Filière modifiée avec succès.'

class ProgramDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    model = Program
    permission_required = 'academics.delete_program'
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('program_list')
    delete_success_message = 'Filière supprimée avec succès.'


class ClassRoomListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ClassRoom
    permission_required = 'academics.view_classroom'
    template_name = 'academics/classroom_list.html'
    context_object_name = 'classrooms'

    def get_queryset(self):
        return ClassRoom.objects.select_related('program')

class ClassRoomCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ClassRoom
    form_class = ClassRoomForm
    permission_required = 'academics.add_classroom'
    template_name = 'academics/classroom_form.html'
    success_url = reverse_lazy('classroom_list')
    success_message = 'Classe ajoutée avec succès.'

class ClassRoomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ClassRoom
    form_class = ClassRoomForm
    permission_required = 'academics.change_classroom'
    template_name = 'academics/classroom_form.html'
    success_url = reverse_lazy('classroom_list')
    success_message = 'Classe modifiée avec succès.'

class ClassRoomDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    model = ClassRoom
    permission_required = 'academics.delete_classroom'
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('classroom_list')
    delete_success_message = 'Classe supprimée avec succès.'


class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    permission_required = 'academics.view_student'
    template_name = 'academics/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        queryset = Student.objects.select_related('program', 'classroom').order_by('last_name', 'first_name')
        q = self.request.GET.get('q', '').strip()
        program_id = self.request.GET.get('program', '').strip()
        classroom_id = self.request.GET.get('classroom', '').strip()
        if q:
            queryset = queryset.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
            )
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.all()
        context['classrooms'] = ClassRoom.objects.select_related('program')
        context['q'] = self.request.GET.get('q', '')
        context['selected_program'] = self.request.GET.get('program', '')
        context['selected_classroom'] = self.request.GET.get('classroom', '')
        return context

class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    permission_required = 'academics.view_student'
    template_name = 'academics/student_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        return Student.objects.select_related('program', 'classroom').prefetch_related('enrollments__course')

class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    permission_required = 'academics.add_student'
    template_name = 'academics/student_form.html'
    success_message = 'Étudiant ajouté avec succès.'

class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    permission_required = 'academics.change_student'
    template_name = 'academics/student_form.html'
    success_message = 'Étudiant modifié avec succès.'

class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    model = Student
    permission_required = 'academics.delete_student'
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('student_list')
    delete_success_message = 'Étudiant supprimé avec succès.'


class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = 'academics.view_course'
    template_name = 'academics/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Course.objects.select_related('program').annotate(student_total=Count('enrollments')).order_by('title')
        q = self.request.GET.get('q', '').strip()
        program_id = self.request.GET.get('program', '').strip()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(code__icontains=q))
        if program_id:
            queryset = queryset.filter(program_id=program_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programs'] = Program.objects.all()
        context['q'] = self.request.GET.get('q', '')
        context['selected_program'] = self.request.GET.get('program', '')
        return context

class CourseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Course
    permission_required = 'academics.view_course'
    template_name = 'academics/course_detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.select_related('program').prefetch_related('enrollments__student')

class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    permission_required = 'academics.add_course'
    template_name = 'academics/course_form.html'
    success_message = 'Cours ajouté avec succès.'

class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    form_class = CourseForm
    permission_required = 'academics.change_course'
    template_name = 'academics/course_form.html'
    success_message = 'Cours modifié avec succès.'

class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    model = Course
    permission_required = 'academics.delete_course'
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('course_list')
    delete_success_message = 'Cours supprimé avec succès.'


class EnrollmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Enrollment
    permission_required = 'academics.view_enrollment'
    template_name = 'academics/enrollment_list.html'
    context_object_name = 'enrollments'
    paginate_by = 12

    def get_queryset(self):
        queryset = Enrollment.objects.select_related('student', 'course', 'course__program')
        q = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '').strip()
        if q:
            queryset = queryset.filter(
                Q(student__first_name__icontains=q)
                | Q(student__last_name__icontains=q)
                | Q(course__title__icontains=q)
                | Q(course__code__icontains=q)
            )
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['status_choices'] = Enrollment.STATUS_CHOICES
        return context

class EnrollmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    permission_required = 'academics.add_enrollment'
    template_name = 'academics/enrollment_form.html'
    success_url = reverse_lazy('enrollment_list')
    success_message = 'Inscription ajoutée avec succès.'

class EnrollmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    permission_required = 'academics.change_enrollment'
    template_name = 'academics/enrollment_form.html'
    success_url = reverse_lazy('enrollment_list')
    success_message = 'Inscription modifiée avec succès.'

class EnrollmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageMixin, DeleteView):
    model = Enrollment
    permission_required = 'academics.delete_enrollment'
    template_name = 'academics/confirm_delete.html'
    success_url = reverse_lazy('enrollment_list')
    delete_success_message = 'Inscription supprimée avec succès.'


@login_required
@permission_required('academics.view_student', raise_exception=True)
def students_by_class_report(request):
    classrooms = ClassRoom.objects.select_related('program').all()
    selected_classroom = None
    students = Student.objects.none()
    classroom_id = request.GET.get('classroom')
    if classroom_id:
        selected_classroom = ClassRoom.objects.filter(pk=classroom_id).select_related('program').first()
        if selected_classroom:
            students = Student.objects.filter(classroom=selected_classroom).select_related('program', 'classroom')
    return render(
        request,
        'academics/students_by_class_report.html',
        {
            'classrooms': classrooms,
            'selected_classroom': selected_classroom,
            'students': students,
        },
    )


@login_required
@permission_required('academics.view_enrollment', raise_exception=True)
def students_by_course_report(request):
    courses = Course.objects.select_related('program').all()
    selected_course = None
    enrollments = Enrollment.objects.none()
    course_id = request.GET.get('course')
    if course_id:
        selected_course = Course.objects.filter(pk=course_id).select_related('program').first()
        if selected_course:
            enrollments = Enrollment.objects.filter(course=selected_course).select_related('student', 'student__classroom')
    return render(
        request,
        'academics/students_by_course_report.html',
        {
            'courses': courses,
            'selected_course': selected_course,
            'enrollments': enrollments,
        },
    )
