from django.urls import path
from . import views

urlpatterns = [
        path('', views.exam_list, name='exam_list'),
        path('add/', views.add_exam, name='add_exam'),
        path('edit/<int:pk>/', views.edit_exam, name='edit_exam'),
        path('delete/<int:pk>/', views.delete_exam, name='delete_exam'),
        path('results/<int:pk>/', views.exam_results, name='exam_results'),
        path('my-results/', views.my_results, name='my_results'),
]