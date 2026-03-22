from django.shortcuts import render
from .models import Drone, Mission, Alerte

def drones_list(request):
    drones = Drone.objects.all()
    return render(request, 'drones/drones_list.html', locals())

def mission_detail(request, pk):
    mission = Mission.objects.get(pk=pk)
    return render(request, 'drones/mission_detail.html', locals())

def alertes_list(request):
    alertes = Alerte.objects.all()
    return render(request, 'drones/alertes_list.html', locals())
