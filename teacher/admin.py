from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'teacher_id', 'email', 'phone', 'department')
    search_fields = ('first_name', 'last_name', 'teacher_id', 'email')
    list_filter = ('gender', 'department', 'joining_date')
    ordering = ('first_name', 'last_name')