from django.shortcuts import render
from motorcycle.models import Motorcycle
from part.models import Part
import random

def welcome(request):
    motorcycles = Motorcycle.objects.all()
    parts = Part.objects.all()
    combined_list = list(motorcycles) + list(parts)
    random.shuffle(combined_list)
    active_group = combined_list[:3]
    other_groups = [combined_list[i:i+3] for i in range(3, len(combined_list), 3)]

    return render(request, 'index.html', {'user': request.user, 'active': active_group, 'others': other_groups})