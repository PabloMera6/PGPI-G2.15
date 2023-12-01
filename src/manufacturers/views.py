from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from newapp.models import Manufacturers as Manufacturer
from motorcycle.models import Motorcycle


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

def view_manufacturer_details(request, manufacturer_id):
    manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
    related_motorcycles = Motorcycle.objects.filter(name__icontains=manufacturer.name)

    return render(request, 'manufacturer_details.html', {'manufacturer': manufacturer, 'motorcycles': related_motorcycles})