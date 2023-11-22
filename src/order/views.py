from django.shortcuts import render, redirect
from .models import Order

def user_orders(request):
    # Asegúrate de que el usuario esté autenticado
    if request.user.is_authenticated:
        # Recupera todas las órdenes del usuario logeado
        orders = Order.objects.filter(buyer=request.user).order_by('-id')

        return render(request, 'user_orders.html', {'orders': orders})
    else:
        # Si el usuario no está autenticado, redirígelos a la página de inicio de sesión
        return redirect('login')  # Ajusta esto según tu URL de inicio de sesión
