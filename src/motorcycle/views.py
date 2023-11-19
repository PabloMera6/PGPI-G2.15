from django.shortcuts import render
from motorcycle.models import Motorcycle

def view_motorcycles(request):
    motorcycles = Motorcycle.objects.all()
    return render(request, 'motorcycles.html', {'motorcycles': motorcycles})