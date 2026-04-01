from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subject
from department.models import Department
from teacher.models import Teacher

@login_required
def subject_list(request):
    subjects = Subject.objects.all().select_related('department', 'teacher')
    return render(request, 'subjects/list_subjects.html', {'subjects': subjects})

@login_required
def subject_create(request):
    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        description = request.POST.get('description', '')

        if Subject.objects.filter(code=code).exists():
            error = "Ce code existe déjà !"
        else:
            Subject.objects.create(
                name=name,
                code=code,
                department_id=department_id,
                teacher_id=teacher_id if teacher_id else None,
                description=description
            )
            return redirect('subject_list')

    return render(request, 'subjects/add_subjects.html', {
        'departments': departments,
        'teachers': teachers,
        'error': error,
    })

@login_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        description = request.POST.get('description', '')

        if Subject.objects.filter(code=code).exclude(pk=pk).exists():
            error = "Ce code existe déjà !"
        else:
            subject.name = name
            subject.code = code
            subject.department_id = department_id
            subject.teacher_id = teacher_id if teacher_id else None
            subject.description = description
            subject.save()
            return redirect('subject_list')

    return render(request, 'subjects/edit_subjects.html', {
        'subject': subject,
        'departments': departments,
        'teachers': teachers,
        'error': error,
    })

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')
    return render(request, 'subjects/delete_subjects.html', {'subject': subject})