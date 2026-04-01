from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_list, name='timetable_list'),
    path('add/', views.timetable_create, name='timetable_create'),
    path('edit/<int:pk>/', views.timetable_update, name='timetable_update'),
    path('delete/<int:pk>/', views.timetable_delete, name='timetable_delete'),
    path('json/', views.timetable_json, name='timetable_json'),
]