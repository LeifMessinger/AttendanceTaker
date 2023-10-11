from django.contrib import admin

from .models import Classroom, Student, AttendanceNote

# Register your models here.
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(AttendanceNote)
