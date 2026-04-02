from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Department
from school.decorators import admin_required, teacher_required, student_required

# Create your views here.

#  1. LISTE 
@login_required
def department_list(request):
    # Récupérer tous les départements triés par nom
    departments = Department.objects.all()
    return render(request, 'departments/departments.html',{'departments': departments})

#  2. AJOUTER 
@admin_required
def add_department(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire

        name = request.POST.get('name')
        head_of_department = request.POST.get('head_of_department')
        description = request.POST.get('description')

        # Vérifier que le nom n'est pas vide
        if not name:
            messages.error(request, 'Le nom est obligatoire !')
            return render(request, 'departments/add-department.html')
        
        # Créer le département dans la base de données
        Department.objects.create(
                                name=name,
                                head_of_department=head_of_department,
                                description=description
                            )
        messages.success(request, 'Département ajouté avec succès !')
        return redirect('department_list')
    
    # GET : afficher le formulaire vide
    return render(request, 'departments/add-department.html')
    
# 3. MODIFIER 
@admin_required
def edit_department(request, pk):
    # Récupérer le département ou afficher 404
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.head_of_department = request.POST.get('head_of_department')
        description = request.POST.get('description')
        department.save()
        messages.success(request, 'Département modifié avec succès !')
        return redirect('department_list')
    
    # GET : afficher le formulaire pré-rempli
    return render(request, 'departments/edit-department.html',{'department': department})
    
#  4. SUPPRIMER 
@admin_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, 'Département supprimé !')
    return redirect('department_list')
