from django.contrib import admin
from .models import Parent, Student

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    search_fields = ('father_name', 'mother_name', 'father_mobile')
    list_filter = ('father_name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id', 'gender', 'student_class', 'section')
    search_fields = ('first_name', 'last_name', 'student_id', 'admission_number')
    list_filter = ('gender', 'student_class', 'section')
    readonly_fields = ('student_image',)
