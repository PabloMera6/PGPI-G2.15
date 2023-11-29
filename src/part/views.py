from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from part.models import Part
from product.models import Product
from rest_framework.views import APIView
from opinion.models import Opinion
from django.db.models import Count, Avg
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

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

class PartDetailView(APIView):
    template_name = 'part_detail.html'
    model = Part

    def get(self, request, *args, **kwargs):
        part = get_object_or_404(self.model, pk=kwargs['part_id'])
        product = get_object_or_404(Product, pk=part.id)

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

        return render(request, 'part_detail.html', {'part': part, 'product': product, 'compatible_motorcycles': compatible_motorcycles, 'not_reviewed': not_reviewed, 'opinions': opinions, 'rating_stats': rating_stats, 'media_scores': media_scores})

    def post(self, request, *args, **kwargs):
        part = get_object_or_404(self.model, pk=kwargs['part_id'])
        product = get_object_or_404(Product, pk=part.id)

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

        return redirect('part_details', part_id=kwargs['part_id'])