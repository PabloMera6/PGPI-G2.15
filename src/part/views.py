from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from part.models import Part

def view_parts(request):
    parts_list = Part.objects.all()

    parts_per_page = 12
    page = request.GET.get('page')
    paginator = Paginator(parts_list, parts_per_page)

    try:
        parts = paginator.page(page)
    except PageNotAnInteger:
        parts = paginator.page(1)
    except EmptyPage:
        parts = paginator.page(paginator.num_pages)

    return render(request, 'parts.html', {'parts': parts})