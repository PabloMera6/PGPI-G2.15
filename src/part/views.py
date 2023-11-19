from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from part.models import Part
from product.models import Product

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

def view_part_details(request, part_id):
    part = get_object_or_404(Part, pk=part_id)
    product = get_object_or_404(Product, pk=part_id)

    category = part.category

    if category == 'Carrocería':
        compatible_motorcycles = part.compatible_carroceria.all()
    elif category == 'Motor':
        compatible_motorcycles = part.compatible_motor.all()
    elif category == 'Transmisión':
        compatible_motorcycles = part.compatible_transmision.all()
    elif category == 'Suspensión':
        compatible_motorcycles = part.compatible_suspension.all()
    elif category == 'Ruedas':
        compatible_motorcycles = part.compatible_ruedas.all()
    elif category == 'Frenos':
        compatible_motorcycles = part.compatible_frenos.all()
    elif category == 'Manillar':
        compatible_motorcycles = part.compatible_manillar.all()
    elif category == 'Sistema de combustible':
        compatible_motorcycles = part.compatible_combustible.all()
    elif category == 'Chasis':
        compatible_motorcycles = part.compatible_chasis.all()
    else:
        compatible_motorcycles = None

    return render(request, 'part_detail.html', {'part': part, 'product': product, 'compatible_motorcycles': compatible_motorcycles})