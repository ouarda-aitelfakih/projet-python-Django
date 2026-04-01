from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from school.decorators import admin_required, teacher_required, student_required
from .models import Exam, ExamResult
from subjects.models import Subject
from student.models import Student

# Create your views here.
@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exams.html', {'exams': exams})

@admin_required
def add_exam(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        Exam.objects.create(name = request.POST.get('name'),
                            subject = Subject.objects.get(pk=request.POST.get('subject')),
                            date = request.POST.get('date'),
                            start_time = request.POST.get('start_time'),
                            end_time = request.POST.get('end_time'),
                            room = request.POST.get('room'),
                            total_marks = request.POST.get('total_marks') or 100,
                                )
        messages.success(request, 'Exam added!')
        return redirect('exam_list')
    return render(request, 'exams/add-exam.html', {'subjects': subjects})

@admin_required
def edit_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    subjects = Subject.objects.all()
    if request.method == 'POST':
        exam.name = request.POST.get('name')
        exam.subject = Subject.objects.get(pk=request.POST.get('subject'))
        exam.date = request.POST.get('date')
        exam.start_time = request.POST.get('start_time')
        exam.end_time = request.POST.get('end_time')
        exam.room = request.POST.get('room')
        exam.total_marks = request.POST.get('total_marks') or 100
        exam.save()
        messages.success(request, 'Exam updated!')
        return redirect('exam_list')
    return render(request, 'exams/edit-exam.html',{'exam': exam, 'subjects': subjects})

@admin_required
def delete_exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    exam.delete()
    messages.success(request, 'Exam deleted!')
    return redirect('exam_list')

@teacher_required
def exam_results(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    students = Student.objects.all()
    existing = {r.student.pk: r for r in ExamResult.objects.filter(exam=exam)}
    
    if request.method == 'POST':
        for student in students:
            marks = request.POST.get(f'marks_{student.pk}')
            if marks:
                ExamResult.objects.update_or_create(
                    exam=exam, student=student,
                    defaults={'marks_obtained': float(marks)}
                )
        messages.success(request, 'Results saved!')
        return redirect('exam_list')
    
    return render(request, 'exams/exam-results.html', {
        'exam': exam,
        'students': students,
        'existing': existing
    })

@student_required
def my_results(request):
    try:
        student = Student.objects.get(user=request.user)
        results = ExamResult.objects.filter(student=student).select_related('exam', 'exam__subject')
        return render(request, 'exams/my-results.html', {'results': results})
    except Student.DoesNotExist:
        messages.error(request, 'No student profile found for your account.')
        return redirect('index')