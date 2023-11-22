from django.shortcuts import render, redirect
from .models import Order
from django.contrib import messages

def user_orders(request):
    # Asegúrate de que el usuario esté autenticado
    if request.user.is_authenticated:
        # Recupera todas las órdenes del usuario logeado
        orders = Order.objects.filter(buyer=request.user).order_by('-id')

        return render(request, 'user_orders.html', {'orders': orders})
    else:
        # Si el usuario no está autenticado, redirígelos a la página de inicio de sesión
        return redirect('login')  # Ajusta esto según tu URL de inicio de sesión
    

def check_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            confirm_url = get_confirm_url(int(order_id))
            return redirect(confirm_url)
        except Order.DoesNotExist:
            messages.error(request, 'El ID de pedido ingresado no existe.')
    
    return render(request, 'check_order_status.html')

def get_confirm_url(order_id):
    return f'/checkout/confirm/confirmed/{order_id}/'
