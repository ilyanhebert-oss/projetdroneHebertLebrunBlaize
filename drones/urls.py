from django.urls import path
from . import views

urlpatterns = [
    path('drones/', views.drones_list, name='drones_list'),
    path('missions/<int:pk>/', views.mission_detail, name='mission_detail'),
    path('alertes/', views.alertes_list, name='alertes_list'),
]