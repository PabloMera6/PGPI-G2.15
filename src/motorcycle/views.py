from part.models import Part
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from motorcycle.models import Motorcycle, DerivedMotorcycle
from product.models import Product
from shop.views import Cart, view_cart
from django.contrib import messages

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

    selected_parts = (
        motorcycle.selected_carrocería,
        motorcycle.selected_motor,
        motorcycle.selected_transmision,
        motorcycle.selected_suspension,
        motorcycle.selected_ruedas,
        motorcycle.selected_frenos,
        motorcycle.selected_manillar,
        motorcycle.selected_combustible,
        motorcycle.selected_chasis
    )

    return render(request, 'motorcycle_detail.html', {'motorcycle': motorcycle, 'product': product, 'compatible_parts': compatible_parts,'selected_parts': selected_parts})


def config(request, motorcycle_id):
    product = get_object_or_404(Product, pk=motorcycle_id)
    motorcycle = get_object_or_404(Motorcycle, pk=motorcycle_id)
    if request.method == 'POST':
        my_cart = Cart(request)
        carroceria =   int(request.POST.get('carroceria'))
        motor =  int(request.POST.get('motor'))
        transmision = int(request.POST.get('transmision'))
        suspension = int(request.POST.get('suspension'))
        ruedas = int(request.POST.get('ruedas'))
        frenos = int(request.POST.get('frenos'))
        manillar = int(request.POST.get('manillar'))
        combustible = int(request.POST.get('combustible'))
        chasis = int(request.POST.get('chasis'))
        my_moto = DerivedMotorcycle(
            base_motorcycle_id=motorcycle_id,
            carroceria_id=carroceria,
            motor_id=motor,
            transmision_id=transmision,
            suspension_id=suspension,
            ruedas_id=ruedas,
            frenos_id=frenos,
            manillar_id=manillar,
            combustible_id=combustible,
            chasis_id=chasis,
            manufacturer_id=product.manufacturer_id,
            reference_number=product.reference_number,
            product_type=product.product_type,
        )
        my_moto.save() 
        my_cart.add(my_moto.id, 1)  
        return view_cart(request)
    else:
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



        return render(request, 'motorcycle_config.html', {'motorcycle': motorcycle, 'product': product, 'compatible_parts': compatible_parts})