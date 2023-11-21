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
        my_cart.add()
    return view_cart(request)

def remove_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        my_cart = Cart(request)
        my_cart.remove(product_id)
    return view_cart(request)

def refresh(request):
    if request.method == 'POST':
        my_cart = Cart(request)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        if quantity < 0:
            messages.error(request,'La cantidad del producto no puede ser menor que 0')
            return redirect('cart')
        elif quantity == 0:
            return remove_cart(request)
        my_cart.refresh(product_id, quantity)
    return view_cart(request)

class Cart():
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self):
        quantity = int(self.request.POST.get('product_quantity'))
        product_id = self.request.POST.get('product_id')
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
        my_cart = self.cart.items()
        if product_id not in my_cart:
            self.cart[product_id] = quantity
        else:
            for key, value in my_cart:
                if key == product_id:
                    value = quantity
                    break
        self.save()


    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True



def checkout(request):
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
                'price': float(product.price) * float(value),
                'quantity': value
            }
        elif product.product_type == 'P':
            part = get_object_or_404(Part, pk=key)
            parts[part] = {
                'price': float(product.price) * float(value),
                'quantity': value
            }

    if request.method == 'POST':
        if precio_total < 30:
            precio_total += 5
        payment_method = request.POST.get('payment_method')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        if payment_method == 'card': 
            request.session['checkout_data'] = {
                'payment_method': payment_method,
                'email': email,
                'full_name': full_name,
                'phone': phone,
                'address': address,
                'total_price': precio_total
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


        order = create_order(precio_total, 'pickup', payment_method, email, full_name, phone, address, my_cart)
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
            'order': order,
        }

        html_message = render_to_string('checkout_confirmation.html', context)
        plain_message = strip_tags(html_message)

        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

        return redirect('/')

    return render(request, 'checkout.html', {
        'motos': motos,
        'parts': parts,
        'manufacturers': manufacturers,
        'precio': round(precio_total, 2)
    })

def create_order(price, shipment, payment, buyer_mail, buyer_name, buyer_phone, address, my_cart):
    order = Order.objects.create(
            price=price,
            shipment=shipment,
            payment=payment,
            buyer_mail=buyer_mail,
            buyer_name=buyer_name,
            buyer_phone=buyer_phone,
            address=address
        )
    for key, value in my_cart.items():
        product = get_object_or_404(Product, pk=key)
        order.products.add(product, through_defaults={'quantity': value})
    return order.id

def confirm(request):
    my_cart = Cart(request).cart
    checkout_data = request.session.get('checkout_data', {})
    payment_method = checkout_data.get('payment_method')
    email = checkout_data.get('email')
    full_name = checkout_data.get('full_name')
    phone = checkout_data.get('phone')
    address = checkout_data.get('address')
    precio_total = checkout_data.get('total_price')
    create_order(precio_total, 'pickup', payment_method, email, full_name, phone, address, my_cart)
    messages.success(request, 'Pago procesado correctamente.')
    del request.session['checkout_data']
    del request.session['cart']
    return redirect('/')