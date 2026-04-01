from django.shortcuts import render, redirect

def index(request):
    return render(request, 'authentication/login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'students/student-dashboard.html')

def student_dashboard(request):
    if request.user.is_authenticated and request.user.is_student:
        return render(request, 'students/student-dashboard.html')
    return redirect('index')

def teacher_dashboard(request):
    if request.user.is_authenticated and request.user.is_teacher:
        return render(request, 'teachers/teacher-dashboard.html')
    return redirect('index')