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

        context = {
            'motorcycle': motorcycle,
            'product': product,
            'compatible_parts': compatible_parts,
            'selected_parts': selected_parts,
            'not_reviewed': not_reviewed,
            'opinions': opinions,
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