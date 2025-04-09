from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, School, Trainer, Attendance, Syllabus, LogBook, Student, Class, StudentAttendance, Performance, LeaveRequest, Assignment, Submission

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(School)
admin.site.register(Trainer)
admin.site.register(Attendance) 
admin.site.register(StudentAttendance) 
admin.site.register(Syllabus)
admin.site.register(LogBook)
admin.site.register(Student)
admin.site.register(Class) 
admin.site.register(Performance)
admin.site.register(LeaveRequest)
admin.site.register(Assignment)
admin.site.register(Submission)

