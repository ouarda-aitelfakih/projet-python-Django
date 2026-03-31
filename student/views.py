from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Student, Parent


#1. LISTE DES ÉTUDIANTS 
def student_list(request):
    # Récupérer TOUS les étudiants depuis la base de données
    students = Student.objects.all()
    # Les envoyer au template
    return render(request, 'students/students.html',  {'student_list': students})

#2. AJOUTER UN ÉTUDIANT
def add_student(request):
    if request.method == 'POST':
        # Récupérer les données de l'étudiant
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # Récupérer les données du parent
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        # 1. Créer et sauvegarder le parent
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )

        # 2. Créer l'étudiant lié au parent
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )

        # 3. Afficher message et rediriger vers la liste
        messages.success(request, 'Student added Successfully')
        return redirect('student_list')

    else:
        return render(request, 'students/add-student.html')


#3. MODIFIER UN ÉTUDIANT
def edit_student(request, student_id):
    # Récupérer l'étudiant à modifier
    student = get_object_or_404(Student, student_id=student_id)
    parent  = student.parent  # Récupérer son parent lié

    if request.method == 'POST':
        # Mettre à jour les données de l'étudiant
        student.first_name       = request.POST.get('first_name')
        student.last_name        = request.POST.get('last_name')
        student.gender           = request.POST.get('gender')
        student.date_of_birth    = request.POST.get('date_of_birth')
        student.student_class    = request.POST.get('student_class')
        student.joining_date     = request.POST.get('joining_date')
        student.mobile_number    = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section          = request.POST.get('section')

         # Si une nouvelle image est uploadée
        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        student.save()  # Sauvegarder l'étudiant

        # Mettre à jour les données du parent
        parent.father_name       = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile     = request.POST.get('father_mobile')
        parent.father_email      = request.POST.get('father_email')
        parent.mother_name       = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile     = request.POST.get('mother_mobile')
        parent.mother_email      = request.POST.get('mother_email')
        parent.present_address   = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')

        parent.save()  # Sauvegarder le parent

        messages.success(request, 'Étudiant modifié avec succès !')
        return redirect('student_list')
    
        # GET : afficher le formulaire pré-rempli
    return render(request, 'students/edit-student.html', {
        'student': student,
        'parent': parent,
    })

    


#4. DÉTAIL D'UN ÉTUDIANT 
def view_student(request, student_id):
    # Chercher l'étudiant avec cet ID, ou afficher erreur 404
    student = get_object_or_404(Student, student_id=student_id)
    
    return render(request, 'students/student-details.html',{'student': student})

#4. SUPPRIMER UN ÉTUDIANT 
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    
    # Supprimer le parent aussi (CASCADE le fait automatiquement
    # mais on supprime le parent pour être explicite)
    parent = student.parent
    student.delete()
    parent.delete()

    messages.success(request, 'Étudiant supprimé avec succès !')
    return redirect('student_list')
    