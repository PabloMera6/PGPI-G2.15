
from part.models import Part
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from motorcycle.models import Motorcycle, DerivedMotorcycle
from product.models import Product
from shop.views import Cart, view_cart
import secrets
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg
from rest_framework.response import Response
from rest_framework import status
from motorcycle.models import Motorcycle
from product.models import Product
from opinion.models import Opinion
from rest_framework.views import APIView


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
        name = "Moto "+my_moto.base_motorcycle.name+" modificada"
        my_moto.name = name
        my_moto.save() 
        my_moto.calculate_deriver_motorcycle_stock()
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

class MotorcycleDetailView(APIView):
    template_name = 'motorcycle_detail.html'
    model = Motorcycle

    def get(self, request, *args, **kwargs):
        motorcycle = get_object_or_404(self.model, pk=kwargs['motorcycle_id'])
        product = get_object_or_404(Product, pk=motorcycle.id)

        not_reviewed = len(Opinion.objects.filter(author=request.user if request.user.is_authenticated else None, product=product)) == 0
        opinions = Opinion.objects.filter(product=product)
        
        rating_stats = []
        media_scores = 0
        if (opinions.count() > 0):
            opinion_counts = Opinion.objects.filter(product=product).values('score').annotate(count=Count('score')).order_by('score')
            total_opinions = Opinion.objects.filter(product=product).count()
            rating_stats = []
            for score in range(1, 6):
                count = next((entry['count'] for entry in opinion_counts if entry['score'] == score), 0)
                percentage = (count / total_opinions) * 100 if total_opinions > 0 else 0
                rating_stats.append((score, count, percentage))

            media_scores = round(opinions.aggregate(avg_score=Avg('score'))['avg_score'], 1)

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

        opinion_dates= {}
        for opinion in opinions:
            opinion_dates[opinion] = {
                'date': opinion.date.strftime('%d-%m-%Y a las %H:%M'),
            }

        context = {
            'motorcycle': motorcycle,
            'product': product,
            'compatible_parts': compatible_parts,
            'selected_parts': selected_parts,
            'not_reviewed': not_reviewed,
            'opinions': opinion_dates,
            'rating_stats': rating_stats,
            'media_scores': media_scores
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        motorcycle = get_object_or_404(self.model, pk=kwargs['motorcycle_id'])
        product = get_object_or_404(Product, pk=motorcycle.id)

        not_reviewed = len(Opinion.objects.filter(author=request.user if request.user.is_authenticated else None, product=product)) == 0

        if request.user.is_authenticated and not_reviewed:
            score = int(request.POST.get('score'))
            description = request.POST.get('description')
            product_id =  int(request.POST.get('product_id'))
            author = request.user

            if not score or not description:
                return Response({'error': 'Puntuación y descripción son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                opinion = Opinion(score=score, description=description, author=author, product_id=product_id)
                opinion.save()
            except IntegrityError:
                return Response({'error': 'Ha ocurrido un error al crear la opinión.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return redirect('motorcycle_details', motorcycle_id=kwargs['motorcycle_id'])