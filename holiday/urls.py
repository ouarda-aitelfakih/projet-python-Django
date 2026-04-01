from django.urls import path
from . import views

urlpatterns = [
    path('', views.holiday_list, name='holiday_list'),
    path('create/', views.holiday_create, name='holiday_create'),
    path('update/<int:pk>/', views.holiday_update, name='holiday_update'),
    path('delete/<int:pk>/', views.holiday_delete, name='holiday_delete'),
]
