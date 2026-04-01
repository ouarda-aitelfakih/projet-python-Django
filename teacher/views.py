from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Teacher
from department.models import Department
from subjects.models import Subject

# Create your views here.
#  1. LISTE 
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teachers.html', {'teachers': teachers})

#  2. VOIR DÉTAIL 
def view_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    return render(request, 'teachers/teacher-details.html', {'teacher': teacher})

# 3. AJOUTER 
def add_teacher(request):
    # On récupère les départements pour le select
    departments = Department.objects.all()
    if request.method == 'POST':
        dept_id = request.POST.get('department')
        dept = Department.objects.get(pk=dept_id) if dept_id else None
        Teacher.objects.create(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            teacher_id = request.POST.get('teacher_id'),
            gender = request.POST.get('gender'),
            date_of_birth = request.POST.get('date_of_birth'),
            email = request.POST.get('email'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address'),
            joining_date = request.POST.get('joining_date'),
            qualification = request.POST.get('qualification'),
            teacher_image = request.FILES.get('teacher_image'),
            department = dept,
        )
        messages.success(request, 'Teacher added successfully!')
        return redirect('teacher_list')
    
    return render(request, 'teachers/add-teacher.html',
            {'departments': departments})

#  4. MODIFIER 
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    departments = Department.objects.all()
    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.gender = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.email = request.POST.get('email')
        teacher.phone = request.POST.get('phone')
        teacher.address = request.POST.get('address')
        teacher.joining_date = request.POST.get('joining_date')
        teacher.qualification = request.POST.get('qualification')
        dept_id = request.POST.get('department')
        teacher.department = Department.objects.get(pk=dept_id) if dept_id else None

        if request.FILES.get('teacher_image'):
            teacher.teacher_image = request.FILES.get('teacher_image')
            teacher.save()
            messages.success(request, 'Teacher updated successfully!')
            return redirect('teacher_list')
    return render(request, 'teachers/edit-teacher.html',{'teacher': teacher, 'departments': departments})

# 5. SUPPRIMER 
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    teacher.delete()
    messages.success(request, 'Teacher deleted successfully!')
    return redirect('teacher_list')