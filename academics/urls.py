from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/add/', views.ProgramCreateView.as_view(), name='program_add'),
    path('programs/<int:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_edit'),
    path('programs/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),

    path('classrooms/', views.ClassRoomListView.as_view(), name='classroom_list'),
    path('classrooms/add/', views.ClassRoomCreateView.as_view(), name='classroom_add'),
    path('classrooms/<int:pk>/edit/', views.ClassRoomUpdateView.as_view(), name='classroom_edit'),
    path('classrooms/<int:pk>/delete/', views.ClassRoomDeleteView.as_view(), name='classroom_delete'),

    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course_add'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/add/', views.EnrollmentCreateView.as_view(), name='enrollment_add'),
    path('enrollments/<int:pk>/edit/', views.EnrollmentUpdateView.as_view(), name='enrollment_edit'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment_delete'),

    path('reports/students-by-class/', views.students_by_class_report, name='students_by_class_report'),
    path('reports/students-by-course/', views.students_by_course_report, name='students_by_course_report'),
]
