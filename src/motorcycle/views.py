from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from motorcycle.models import Motorcycle
from product.models import Product

def view_motorcycles(request):
    motorcycles_list = Motorcycle.objects.all()

    motorcycles_per_page = 12
    page = request.GET.get('page')
    paginator = Paginator(motorcycles_list, motorcycles_per_page)

    try:
        motorcycles = paginator.page(page)
    except PageNotAnInteger:
        motorcycles = paginator.page(1)
    except EmptyPage:
        motorcycles = paginator.page(paginator.num_pages)

    return render(request, 'motorcycles.html', {'motorcycles': motorcycles})

def view_motorcycle_details(request, motorcycle_id):
    motorcycle = get_object_or_404(Motorcycle, pk=motorcycle_id)
    product = get_object_or_404(Product, pk=motorcycle_id)

    compatible_parts = (
        motorcycle.compatible_carroceria.all() |
        motorcycle.compatible_motor.all() |
        motorcycle.compatible_transmision.all() |
        motorcycle.compatible_suspension.all() |
        motorcycle.compatible_ruedas.all() |
        motorcycle.compatible_frenos.all() |
        motorcycle.compatible_manillar.all() |
        motorcycle.compatible_combustible.all() |
        motorcycle.compatible_chasis.all()
    ).distinct()

    return render(request, 'motorcycle_detail.html', {'motorcycle': motorcycle, 'product': product, 'compatible_parts': compatible_parts})