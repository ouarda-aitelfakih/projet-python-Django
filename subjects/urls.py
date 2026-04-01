from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('add/', views.subject_create, name='subject_create'),
    path('edit/<int:pk>/', views.subject_update, name='subject_update'),
    path('delete/<int:pk>/', views.subject_delete, name='subject_delete'),
]