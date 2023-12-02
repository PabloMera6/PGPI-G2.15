# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Claim
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def create_claim(request):
    if request.user.is_staff:
        return HttpResponseForbidden("Acceso prohibido. No puedes crear reclamaciones como administrador.")
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if description:
            claim = Claim.objects.create(author=request.user, description=description, title=title)
            return redirect('initial')
        else:
            messages.error(request, 'La descripción de la reclamación no puede estar vacía.')

    return render(request, 'create_claim.html')


@login_required
def view_claims(request):
    if request.user.is_staff:
        claims = Claim.objects.all()
        return render(request, 'view_claims.html', {'claims': claims})
    else:
        return redirect('initial') 
    

@login_required
def view_claim(request, claim_id):
    if not request.user.is_superuser:
        return redirect('initial')

    claim = get_object_or_404(Claim, id=claim_id)

    if request.method == 'POST':
        response_text = request.POST.get('response_text')
        claim.response = response_text
        claim.save()
        
        return redirect('view_claims')
    
    claim_formated = claim.date.strftime('%d-%m-%Y a las %H:%M')

    return render(request, 'view_claim.html', {'claim': claim, 'claim_formated': claim_formated})

@login_required
def user_view_claims(request):
    claims = Claim.objects.filter(author=request.user)

    return render(request, 'user_view_claims.html', {'claims': claims})

@login_required
def user_view_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)

    claim_formated = claim.date.strftime('%d-%m-%Y a las %H:%M')

    return render(request, 'user_view_claim.html', {'claim': claim, 'claim_formated': claim_formated})