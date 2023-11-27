from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Order
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from manufacturer.models import Manufacturer
from order.models import Order,OrderProduct
from product.models import Product
from motorcycle.models import Motorcycle
from part.models import Part

def user_orders(request):

    if request.user.is_authenticated:

        orders = Order.objects.filter(buyer=request.user).order_by('-id')

        return render(request, 'user_orders.html', {'orders': orders})
    else:
        return redirect('login') 
    

def check_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            confirm_url = get_confirm_url(order_id)
            return redirect(confirm_url)
        except (Http404, Order.DoesNotExist, ValidationError):
            messages.error(request, 'El ID de pedido ingresado no existe.')
    
    return render(request, 'check_order_status.html')

def get_confirm_url(order_id):
    order = Order.objects.get(id=order_id)
    return f'/order/checkout/confirm/confirmed/{order.id}/'


def administrate(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'administrate.html', {'user': request.user})
    else:
        return redirect('/')

def orders(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all().order_by('-id')
        return render(request, 'orders.html', {'orders': orders})
    else:
        return redirect('/')
    
def administrate_order(request, order_id):
    if request.user.is_authenticated and request.user.is_superuser:
        order = get_object_or_404(Order, pk=order_id)
        manufacturers = Manufacturer.objects.all()
        op = OrderProduct.objects.filter(order=order)
        motos = {}
        parts = {}
        for x in op:
            product = x.product
            if product.product_type == 'M':
                moto = get_object_or_404(Motorcycle, pk=product.id)
                motos[moto] = {
                    'price': float(product.price) * float(x.quantity),
                    'quantity': x.quantity
                }
            elif product.product_type == 'P':
                part = get_object_or_404(Part, pk=product.id)
                parts[part] = {
                    'price': float(product.price) * float(x.quantity),
                    'quantity': x.quantity
                }
        if request.method == 'POST':
            order.state = request.POST.get('state')
            order.save()
            messages.success(request, 'Estado de pedido actualizado correctamente.')
            return redirect('orders')
        return render(request, 'administrate_order.html', {'order': order,
            'motos': motos,
            'parts': parts,
            'order': order,
            'manufacturers': manufacturers})
    else:
        return redirect('/')