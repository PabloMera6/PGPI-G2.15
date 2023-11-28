from part.models import Part
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from motorcycle.models import Motorcycle, DerivedMotorcycle
from product.models import Product
from shop.views import Cart, view_cart
from django.contrib import messages
import secrets

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

def generate_reference_number():
    reference_number = secrets.token_hex(7).upper()[:15]
    return reference_number

def config(request, motorcycle_id):
    product = get_object_or_404(Product, pk=motorcycle_id)
    motorcycle = get_object_or_404(Motorcycle, pk=motorcycle_id)
    if request.method == 'POST':
        my_cart = Cart(request)
        reference_number = product.reference_number + "-"
        carroceria =   get_object_or_404(Part, pk=int(request.POST.get('carroceria')))
        motor = get_object_or_404(Part, pk=int(request.POST.get('motor')))
        transmision = get_object_or_404(Part, pk=int(request.POST.get('transmision')))
        suspension = get_object_or_404(Part, pk=int(request.POST.get('suspension')))
        ruedas = get_object_or_404(Part, pk=int(request.POST.get('ruedas')))
        frenos = get_object_or_404(Part, pk=int(request.POST.get('frenos')))
        manillar = get_object_or_404(Part, pk=int(request.POST.get('manillar')))
        combustible = get_object_or_404(Part, pk=int(request.POST.get('combustible')))
        chasis = get_object_or_404(Part, pk=int(request.POST.get('chasis')))

        reference_number = generate_reference_number()
        while True:
            reference_number = generate_reference_number()
            if not Product.objects.filter(reference_number=reference_number).exists():
                break
        price = motorcycle.price
        price += carroceria.price
        price += motor.price
        price += transmision.price
        price += suspension.price
        price += ruedas.price
        price += frenos.price
        price += manillar.price
        price += combustible.price
        price += chasis.price
        price -= motorcycle.selected_carrocería.price
        price -= motorcycle.selected_motor.price
        price -= motorcycle.selected_transmision.price
        price -= motorcycle.selected_suspension.price
        price -= motorcycle.selected_ruedas.price
        price -= motorcycle.selected_frenos.price
        price -= motorcycle.selected_manillar.price
        price -= motorcycle.selected_combustible.price
        price -= motorcycle.selected_chasis.price
        my_moto = DerivedMotorcycle (
            base_motorcycle_id=motorcycle_id,
            carroceria_id=carroceria.id,
            motor_id=motor.id,
            transmision_id=transmision.id,
            suspension_id=suspension.id,
            ruedas_id=ruedas.id,
            frenos_id=frenos.id,
            manillar_id=manillar.id,
            combustible_id=combustible.id,
            chasis_id=chasis.id,
            manufacturer_id=product.manufacturer_id,
            product_type='C',
            price = price,
            reference_number=reference_number,
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