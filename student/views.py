from django.shortcuts import render

# Create your views here.
def student_list(request):
    return render(request, 'student/student_list.html')
def add_student(request):
    return render(request, 'student/add_student.html')