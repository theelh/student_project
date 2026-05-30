from django.contrib import admin

from .models import ClassRoom, Course, Enrollment, Program, Student


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'program')
    list_filter = ('program', 'level')
    search_fields = ('name', 'level', 'program__name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'program', 'credits', 'enrolled_students_count')
    list_filter = ('program',)
    search_fields = ('title', 'code', 'program__name')


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'program', 'classroom')
    list_filter = ('program', 'classroom')
    search_fields = ('last_name', 'first_name', 'email')
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrolled_at')
    list_filter = ('status', 'course__program', 'course')
    search_fields = ('student__last_name', 'student__first_name', 'course__title', 'course__code')
