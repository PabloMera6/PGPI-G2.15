from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manufacturer.models import Manufacturer


def view_manufacturers(request):
    manufacturers_list = Manufacturer.objects.all()

    manufacturers_per_page = 12
    page = request.GET.get('page')
    paginator = Paginator(manufacturers_list, manufacturers_per_page)

    try:
        manufacturers = paginator.page(page)
    except PageNotAnInteger:
        manufacturers = paginator.page(1)
    except EmptyPage:
        manufacturers = paginator.page(paginator.num_pages)

    return render(request, 'manufacturers.html', {'manufacturers': manufacturers})