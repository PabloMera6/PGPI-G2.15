from product.models import Product
from django.shortcuts import redirect, render
from motorcycle.models import Motorcycle
from manufacturer.models import Manufacturer 
from part.models import Part
from django.views.generic import TemplateView
from manufacturer.models import Manufacturer
from .forms import SearchForm
import random
from django.shortcuts import get_object_or_404
from django.contrib import messages
from order.models import Order
from order.models import OrderProduct
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from paypalrestsdk import Payment


def welcome(request):
    motorcycles = Motorcycle.objects.all()
    parts = Part.objects.all()
    combined_list = list(motorcycles) + list(parts)
    random.shuffle(combined_list)
    active_group = combined_list[:3]
    other_groups = [combined_list[i:i+3] for i in range(3, len(combined_list), 3)]

    return render(request, 'index.html', {'user': request.user, 'active': active_group, 'others': other_groups})

def search(request):
    motorcycles = parts = manufacturers = ''
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_type = form.cleaned_data['search_type']
            if search_type == 'all':
                motorcycles = Motorcycle.objects.filter(name__icontains=query)
                parts = Part.objects.filter(name__icontains=query)
                manufacturers = Manufacturer.objects.filter(name__icontains=query)
            elif search_type == 'motorcycles':
                motorcycles = Motorcycle.objects.filter(name__icontains=query)
            elif search_type == 'parts':
                parts = Part.objects.filter(name__icontains=query)
            elif search_type == 'manufacturers':
                manufacturers = Manufacturer.objects.filter(name__icontains=query)
        else:
            search_type = request.GET.get('search_type', 'all')
            if search_type == 'all':
                motorcycles = Motorcycle.objects.all()
                parts = Part.objects.all()
                manufacturers = Manufacturer.objects.all()
            elif search_type == 'motorcycles':
                motorcycles = Motorcycle.objects.all()
            elif search_type == 'parts':
                parts = Part.objects.all()
            elif search_type == 'manufacturers':
                manufacturers = Manufacturer.objects.all()
    else:
        form = SearchForm()
        motorcycles = Motorcycle.objects.all()
        parts = Part.objects.all()
        manufacturers = Manufacturer.objects.all()

    results = list(motorcycles) + list(parts) + list(manufacturers)
    results = sorted(results, key=lambda x: getattr(x, 'name'))
    return render(request, 'search.html', {'form': form, 'results': results, 'user': request.user})

def checkout(request):
    my_cart = Cart(request).cart
    motos = {}
    parts = {}
    manufacturers = Manufacturer.objects.all()
    precio_total = 0.0
    user = request.user if request.user.is_authenticated else None

    for key, value in my_cart.items():
        product = get_object_or_404(Product, pk=key)
        precio_total += float(product.price) * float(value)
        if product.product_type == 'M':
            moto = get_object_or_404(Motorcycle, pk=key)
            motos[moto] = {
                'price': float(product.price) * float(value),
                'quantity': value
            }
        elif product.product_type == 'P':
            part = get_object_or_404(Part, pk=key)
            parts[part] = {
                'price': float(product.price) * float(value),
                'quantity': value
            }
    if precio_total < 30:
            precio_total += 5
    if request.method == 'POST':
        for key, value in my_cart.items():
            product = get_object_or_404(Product, pk=key)
            if product.product_type == 'P':
                part = get_object_or_404(Part, pk=key)
                if part.stock_quantity < value:
                    messages.error(request, f"No hay suficiente stock del producto {part.name}")
                    return redirect('/checkout/')
            elif product.product_type == 'M':
                moto = get_object_or_404(Motorcycle, pk=key)
                moto.calculate_motorcicle_stock()
                if moto.stock_quantity < value:
                    messages.error(request, f"No hay suficiente stock del producto {moto.name}")
                    return redirect('/checkout/')
        
        payment_method = request.POST.get('payment_method')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        if payment_method == 'Tarjeta' or payment_method == 'card': 
            request.session['checkout_data'] = {
                'payment_method': payment_method,
                'email': email,
                'full_name': full_name,
                'phone': phone,
                'address': address,
                'total_price': precio_total,
                'city': city,
                'postal_code': postal_code
            }
            paypal_payment = Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": str(precio_total),
                        "currency": "EUR"
                    },
                    "description": "Descripción del pago"
                }],
                "redirect_urls": {
                    "return_url": request.build_absolute_uri('/checkout/confirm/'),
                    "cancel_url": request.build_absolute_uri('/checkout/confirm/')
                }
            })

            if paypal_payment.create():
                return redirect(paypal_payment.links[1]['href'])
            else:
                messages.error(request, 'Error al procesar el pago con PayPal.')
                return redirect('/checkout/')


        order = create_order(precio_total, 'pickup', payment_method, email, full_name, phone, address, my_cart,city,postal_code,user)
        order_id = order.id
        del request.session['cart']
        messages.success(request, 'Pedido creado exitosamente.')
        subject = 'Detalles de tu compra en Motos Para Todos'
        from_email = 'motosparatodos@outlook.es'
        to_email = [email]

        context = {
            'full_name': full_name,
            'precio_total': precio_total,
            'motos': motos,
            'parts': parts,
            'payment_method': payment_method,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'order': order_id,
        }

        html_message = render_to_string('checkout_confirmation.html', context)
        plain_message = strip_tags(html_message)

        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)


        return redirect(f'/checkout/confirm/confirmed/{order.id}/')

    return render(request, 'checkout.html', {
        'motos': motos,
        'parts': parts,
        'manufacturers': manufacturers,
        'precio': round(precio_total, 2)
    })

def create_order(price, shipment, payment, buyer_mail, buyer_name, buyer_phone, address, my_cart,city,postal_code,user):
    order = Order.objects.create(
            price=price,
            shipment=shipment,
            payment=payment,
            buyer_mail=buyer_mail,
            buyer_name=buyer_name,
            buyer_phone=buyer_phone,
            address=address,
            city=city,
            postal_code=postal_code
        )
    if user != None:
        order.buyer = user
        order.save()
    for key, value in my_cart.items():
        product = get_object_or_404(Product, pk=key)
        order.products.add(product, through_defaults={'quantity': value})
        if product.product_type == 'P':
            part = get_object_or_404(Part, pk=key)
            part.stock_quantity -= value
            part.save()
        elif product.product_type == 'M':
            moto = get_object_or_404(Motorcycle, pk=key)
            moto.calculate_motorcicle_stock()
            moto.update_motorcicle_stock(value)
            moto.save()
    return order

def confirm(request):
    user = request.user if request.user.is_authenticated else None
    my_cart = Cart(request).cart
    checkout_data = request.session.get('checkout_data', {})
    payment_method = checkout_data.get('payment_method')
    email = checkout_data.get('email')
    full_name = checkout_data.get('full_name')
    phone = checkout_data.get('phone')
    address = checkout_data.get('address')
    precio_total = checkout_data.get('total_price')
    city = checkout_data.get('city')
    postal_code = checkout_data.get('postal_code')
    order = create_order(precio_total, 'pickup', payment_method, email, full_name, phone, address, my_cart,city,postal_code,user)
    messages.success(request, 'Pago procesado correctamente.')
    del request.session['checkout_data']
    del request.session['cart']
    return redirect(f'/checkout/confirm/confirmed/{order.id}/')

def confirmed(request, order_id):
    manufacturers = Manufacturer.objects.all()
    order = get_object_or_404(Order, pk=order_id)
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
    return render(request, 'order_resume.html',{'motos': motos,
        'parts': parts,
        'order': order,
        'manufacturers': manufacturers,})

def view_cart(request):
    my_cart = Cart(request).cart
    motos = {}
    parts = {}
    manufacturers = Manufacturer.objects.all()
    precio_total = 0.0
    for key, value in my_cart.items():
        product = get_object_or_404(Product, pk=key)
        precio_total += float(product.price) * float(value)
        if product.product_type == 'M':
            moto = get_object_or_404(Motorcycle, pk=key)
            motos[moto] = {
                'price': round(float(product.price) * float(value), 2),
                'quantity': value
            }
        elif product.product_type == 'P':
            part = get_object_or_404(Part, pk=key)
            parts[part] = {
                'price': round(float(product.price) * float(value), 2),
                'quantity': value
            }
    return render(request, 'cart.html', {
        'motos': motos,
        'parts': parts,
        'manufacturers': manufacturers,
        'precio': round(precio_total, 2)
    })

def add_to_cart(request):
    if request.method == 'POST':
        my_cart = Cart(request)
        quantity = int(request.POST.get('product_quantity'))
        product_id = request.POST.get('product_id')
        if not my_cart.check_stock(product_id, quantity, already_in_cart=True):
            product = get_object_or_404(Product, pk=product_id)
            if product.product_type == 'P':
                part = get_object_or_404(Part, pk=product_id)
                messages.error(request,f"No hay suficiente stock del producto: {part.name}")
                return redirect('cart')
            elif product.product_type == 'M':
                moto = get_object_or_404(Motorcycle, pk=product_id)
                messages.error(request,f"No hay suficiente stock del producto: {moto.name}")
                return redirect('cart')
        my_cart.add(product_id, quantity)
    return view_cart(request)

def remove_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        my_cart = Cart(request)
        my_cart.remove(product_id)
    return view_cart(request)

def refresh_cart(request):
    if request.method == 'POST':
        my_cart = Cart(request)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        if quantity < 0:
            messages.error(request,'La cantidad del producto no puede ser menor que 0')
            return redirect('cart')
        elif quantity == 0:
            return remove_cart(request)
        elif not my_cart.check_stock(product_id, quantity):
            product = get_object_or_404(Product, pk=product_id)
            if product.product_type == 'P':
                part = get_object_or_404(Part, pk=product_id)
                messages.error(request,f"No hay suficiente stock del producto: {part.name}")
                return redirect('cart')
            elif product.product_type == 'M':
                moto = get_object_or_404(Motorcycle, pk=product_id)
                messages.error(request,f"No hay suficiente stock del producto: {moto.name}")
                return redirect('cart')
        my_cart.refresh(product_id, quantity)
    return view_cart(request)

class Cart():
    #Clase en la que se encuentran distintos metodos para trabajar con el carrito de la compra
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def check_stock(self, product_id, quantity, already_in_cart=False):
        # Already in cart significa que quiere comprobar el stock con la cantidad que ya esta en el carrito
        product = get_object_or_404(Product, pk=product_id)
        if already_in_cart:
            for key, value in self.cart.items():
                    if key == product_id:
                        value = value + quantity
                        if product.product_type == 'P':
                            part = get_object_or_404(Part, pk=product_id)
                            if part.stock_quantity < value :
                                return False
                        elif product.product_type == 'M':
                            moto = get_object_or_404(Motorcycle, pk=product_id)
                            if moto.stock_quantity < value:
                                return False
                        break
        else:
            if product.product_type == 'P':
                part = get_object_or_404(Part, pk=product_id)
                if part.stock_quantity < quantity:
                    return False
            elif product.product_type == 'M':
                moto = get_object_or_404(Motorcycle, pk=product_id)
                if moto.stock_quantity < quantity:
                    return False
        return True

    def add(self, product_id, quantity=1):
        if product_id not in self.cart.keys():
            self.cart[product_id] = quantity
        else:
            for key, value in self.cart.items():
                if key == product_id:
                    value = value + quantity
                    self.cart[product_id] = value
                    break
        self.save()

    def remove(self, product_id=None):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        elif product_id == None:
            self.session["cart"] = {}
            self.session.modified = True

    def refresh(self, product_id, quantity):
        self.cart[product_id] = quantity
        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True