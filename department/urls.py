from django.urls import path
from . import views


urlpatterns = [
    # Liste : http://localhost:8000/department/
    path('', views.department_list, name='department_list'),

    # Ajouter : http://localhost:8000/department/add/
    path('add/', views.add_department, name='add_department'),

    # Modifier : http://localhost:8000/department/edit/1/
    path('edit/<int:pk>/', views.edit_department, name='edit_department'),
    
    # Supprimer : http://localhost:8000/department/delete/1/
    path('delete/<int:pk>/', views.delete_department, name='delete_department'),
]