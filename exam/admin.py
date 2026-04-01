from django.contrib import admin
from .models import Exam, ExamResult
# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date', 'total_marks')
    search_fields = ('name', 'subject__name')
    list_filter = ('subject', 'date')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'marks_obtained', 'grade')
    search_fields = ('exam__name', 'student__first_name')
    list_filter = ('exam', 'grade')