from product.models import Product
from django.shortcuts import redirect, render
from django.db.models import Avg
from opinion.models import Opinion
from motorcycle.models import Motorcycle, DerivedMotorcycle
from newapp.models import Manufacturers as Manufacturer
from part.models import Part
from django.views.generic import TemplateView

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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from paypalrestsdk import Payment


def welcome(request):
    motorcycles = Motorcycle.objects.filter(show=True)
    parts = Part.objects.filter(show=True)
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
            min_price = form.cleaned_data['min_price'] or 0
            max_price = form.cleaned_data['max_price'] or 99999999
            score = form.cleaned_data['score'] or 0
            products = Product.objects.all()
            p_ids = {}
            for product in products:
                score_avg = Opinion.objects.filter(product=product).aggregate(Avg('score'))['score__avg']
                if score_avg != None:
                    p_ids[product.id] = round(score_avg,1)
            prod_ids = dict(p_ids)
            for key, value in p_ids.items():
                if value != score:
                    del prod_ids[key]
            related_products = Product.objects.filter(id__in=prod_ids.keys())
            related_motorcycles = set(Motorcycle.objects.filter(id__in=related_products))
            related_parts = set(Part.objects.filter(id__in=related_products))
            if min_price > max_price:
                messages.error(request, 'El precio mínimo no puede ser mayor que el precio máximo.')
                return redirect('/search/')
            elif min_price < 0 or max_price < 0:
                messages.error(request, 'Los precios no pueden ser negativos.')
                return redirect('/search/')
            if search_type == 'all':
                motorcycles = Motorcycle.objects.filter(name__icontains=query, price__range=(min_price, max_price))
                parts = Part.objects.filter(name__icontains=query, price__range=(min_price, max_price))
                manufacturers = Manufacturer.objects.filter(name__icontains=query)
            elif search_type == 'motorcycles':
                motorcycles = Motorcycle.objects.filter(name__icontains=query, price__range=(min_price, max_price))
            elif search_type == 'parts':
                parts = Part.objects.filter(name__icontains=query, price__range=(min_price, max_price))
            elif search_type == 'manufacturers':
                manufacturers = Manufacturer.objects.filter(name__icontains=query)
        else:
            search_type = request.GET.get('search_type', 'all')
            min_price = float(request.GET.get('min_price')) if request.GET.get('min_price') else None
            max_price = float(request.GET.get('max_price')) if request.GET.get('max_price') else None
            score = float(request.GET.get('score')) if request.GET.get('score') else None
            products = Product.objects.all()
            p_ids = {}
            for product in products:
                score_avg = Opinion.objects.filter(product=product).aggregate(Avg('score'))['score__avg']
                if score_avg != None:
                    p_ids[product.id] = round(score_avg,1)
            prod_ids = dict(p_ids)
            for key, value in p_ids.items():
                if value != score:
                    del prod_ids[key]
            related_products = Product.objects.filter(id__in=prod_ids.keys())
            related_motorcycles = set(Motorcycle.objects.filter(id__in=related_products))
            related_parts = set(Part.objects.filter(id__in=related_products))
            if min_price == None and max_price == None:
                min_price = 0
                max_price = 99999999
            elif min_price == None:
                min_price = 0
            elif max_price == None:
                max_price = 99999999
            elif min_price > max_price:
                messages.error(request, 'El precio mínimo no puede ser mayor que el precio máximo.')
                return redirect('/search/')
            elif min_price < 0 or max_price < 0:
                messages.error(request, 'Los precios no pueden ser negativos.')
                return redirect('/search/')
            if search_type == 'all':
                motorcycles = Motorcycle.objects.filter(price__range=(min_price, max_price))
                parts = Part.objects.filter(price__range=(min_price, max_price))
                manufacturers = Manufacturer.objects.all()
            elif search_type == 'motorcycles':
                motorcycles = Motorcycle.objects.filter(price__range=(min_price, max_price))
            elif search_type == 'parts':
                parts = Part.objects.filter(price__range=(min_price, max_price))
            elif search_type == 'manufacturers':
                manufacturers = Manufacturer.objects.all()
    else:
        form = SearchForm()
        motorcycles = Motorcycle.objects.all()
        parts = Part.objects.all()
        manufacturers = Manufacturer.objects.all()

    if(score != 0):
        motorcycles = list(related_motorcycles.intersection(motorcycles))
        parts = list(related_parts.intersection(parts))

    if search_type == 'all':
        results = list(motorcycles) + list(parts)
    else:
        results = list(motorcycles) + list(parts) + list(manufacturers)
    results = sorted(results, key=lambda x: getattr(x, 'name'))

    results_per_page = 12
    page = request.GET.get('page')
    paginator = Paginator(results, results_per_page)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'search.html', {'form': form, 'results': results, 'user': request.user})

def checkout(request):
    my_cart = Cart(request).cart
    motos = {}
    parts = {}
    derived_motos = {}
    manufacturers = Manufacturer.objects.all()
    precio_total = 0.0
    user = request.user if request.user.is_authenticated else None

    for key, value in my_cart.items():
        product = get_object_or_404(Product, pk=key)
        precio_total += round(float(product.price) * float(value), 2)
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
        if product.product_type == 'C':
            derived_moto = get_object_or_404(DerivedMotorcycle, pk=key)
            derived_motos[derived_moto] = {
                'price': round(float(product.price) * float(value), 2),
                'quantity': value
            }
    if precio_total == 0:
        messages.error(request, 'No puedes realizar un pedido sin productos.')
        return redirect('cart')
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
                #moto.calculate_motorcicle_stock()
                if moto.stock_quantity < value:
                    messages.error(request, f"No hay suficiente stock del producto {moto.name}")
                    return redirect('/checkout/')
            elif product.product_type == 'C':
                derived_moto = get_object_or_404(DerivedMotorcycle, pk=key)
                derived_moto.calculate_deriver_motorcycle_stock()
                if derived_moto.stock_quantity < value:
                    messages.error(request, f"No hay suficiente stock de piezas de la moto que has configurado, cambia los componentes o reduce la cantidad de motos a comprar")
                    return redirect('/checkout/')
        payment_method = request.POST.get('payment_method')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        shipment = request.POST.get('shipment')
        if precio_total <30 and shipment == 'Envío a domicilio':
            precio_total += 5
        if payment_method == 'Tarjeta' or payment_method == 'card': 
            request.session['checkout_data'] = {
                'payment_method': payment_method,
                'email': email,
                'full_name': full_name,
                'phone': phone,
                'address': address,
                'total_price': precio_total,
                'city': city,
                'postal_code': postal_code,
                'shipment': shipment,

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


        order = create_order(precio_total, shipment, payment_method, email, full_name, phone, address, my_cart,city,postal_code,user)
        order_id = order.id
        del request.session['cart']
        


        return redirect(f'/checkout/confirm/confirmed/{order.id}/')

    return render(request, 'checkout.html', {
        'motos': motos,
        'parts': parts,
        'derived_motos': derived_motos,
        'manufacturers': manufacturers,
        'precio': round(precio_total, 2)
    })

def enviar_correo(full_name, precio_total, motos, parts, payment_method, address, city, postal_code, order_id, email):
    try:
        order = get_object_or_404(Order, pk=order_id)
        shipment = order.shipment
        subject = 'Detalles de tu compra en Motos Para Todos'
        from_email = 'motosparatodos@outlook.es'
        to_email = [email]

        context = {
            'full_name': full_name,
            'precio_total': round(precio_total, 2),
            'motos': motos,
            'parts': parts,
            'payment_method': payment_method,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'order': order_id,
            'shipment': shipment,
            }

        html_message = render_to_string('checkout_confirmation.html', context)
        plain_message = strip_tags(html_message)

        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
    except:
        pass

def create_order(price, shipment, payment, buyer_mail, buyer_name, buyer_phone, address, my_cart,city,postal_code,user):
    parts = {}
    motos = {}
    derived_motos = {}
    order = Order.objects.create(
            price=price,
            shipment=shipment,
            payment=payment,
            buyer_mail=buyer_mail,
            buyer_name=buyer_name,
            buyer_phone=buyer_phone,
            address=address,
            city=city,
            postal_code=postal_code,
            state="Pendiente"
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
            parts[part] = {
                'price': round(float(product.price) * float(value), 2),
                'quantity': value
            }
        elif product.product_type == 'M':
            moto = get_object_or_404(Motorcycle, pk=key)
            moto.stock_quantity -= value
            motos[moto] = {
                'price': round(float(product.price) * float(value), 2),
                'quantity': value
            }
            #moto.calculate_motorcicle_stock()
            #moto.update_motorcicle_stock(value)
            moto.save()
        if product.product_type == 'C':
            derived_moto = get_object_or_404(DerivedMotorcycle, pk=key)
            derived_moto.update_deriver_motorcycle_stock(value)
            motos[derived_moto] = {
                'price': round(float(product.price) * float(value), 2),
                'quantity': value
            }
    
    enviar_correo(buyer_name, price, motos, parts, payment, address, city, postal_code, order.id, buyer_mail)
        
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
    shipment = checkout_data.get('shipment')
    order = create_order(precio_total, shipment, payment_method, email, full_name, phone, address, my_cart,city,postal_code,user)
    #messages.success(request, 'Pago procesado correctamente.')
    del request.session['checkout_data']
    del request.session['cart'] 
    return redirect(f'/checkout/confirm/confirmed/{order.id}/')

def confirmed(request, order_id):
    manufacturers = Manufacturer.objects.all()
    order = get_object_or_404(Order, pk=order_id)
    op = OrderProduct.objects.filter(order=order)
    motos = {}
    parts = {}
    derived_motos = {}
    for x in op:
        product = x.product
        if product.product_type == 'M':
            moto = get_object_or_404(Motorcycle, pk=product.id)
            motos[moto] = {
                'price': round(float(product.price) * float(x.quantity), 2),
                'quantity': x.quantity
            }
        elif product.product_type == 'P':
            part = get_object_or_404(Part, pk=product.id)
            parts[part] = {
                'price': round(float(product.price) * float(x.quantity), 2),
                'quantity': x.quantity
            }
        if product.product_type == 'C':
            derived_moto = get_object_or_404(DerivedMotorcycle, pk=product.id)
            derived_motos[derived_moto] = {
                'price': round(float(product.price) * float(x.quantity), 2),
                'quantity': x.quantity
            }
    return render(request, 'order_resume.html',{'motos': motos,
        'parts': parts,
        'order': order,
        'derived_motos': derived_motos,
        'manufacturers': manufacturers,})

def view_cart(request):
    my_cart = Cart(request).cart
    motos = {}
    parts = {}
    derived_motos = {}
    manufacturers = Manufacturer.objects.all()
    precio_total = 0.0
    for key, value in my_cart.items():
        product = get_object_or_404(Product, pk=key)
        precio_total += round(float(product.price) * float(value), 2)
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
        if product.product_type == 'C':
            derived_moto = get_object_or_404(DerivedMotorcycle, pk=key)
            derived_motos[derived_moto] = {
                'price': round(float(product.price) * float(value), 2),
                'quantity': value
            }
    return render(request, 'cart.html', {
        'motos': motos,
        'parts': parts,
        'derived_motos': derived_motos,
        'manufacturers': manufacturers,
        'precio': round(precio_total, 2)
    })

def add_to_cart(request):
    if request.method == 'POST':
        my_cart = Cart(request)
        quantity = int(request.POST.get('product_quantity')) if request.POST.get('product_quantity') else 1
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
            if product.product_type == 'C':
                derived_moto = get_object_or_404(DerivedMotorcycle, pk=product_id)
                messages.error(request,f"No hay suficiente stock de piezas de la moto que has configurado, cambia los componentes o reduce la cantidad de motos a comprar")
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
            if product.product_type == 'C':
                derived_moto = get_object_or_404(DerivedMotorcycle, pk=product_id)
                messages.error(request,f"No hay suficiente stock de piezas de la moto que has configurado, cambia los componentes o reduce la cantidad de motos a comprar")
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
                        if product.product_type == 'C':
                            derived_moto = get_object_or_404(DerivedMotorcycle, pk=product_id)
                            derived_moto.calculate_deriver_motorcycle_stock
                            if derived_moto.stock_quantity < value:
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
            elif product.product_type == 'C':
                derived_moto = get_object_or_404(DerivedMotorcycle, pk=product_id)
                derived_moto.calculate_deriver_motorcycle_stock
                print(derived_moto.stock_quantity)
                if derived_moto.stock_quantity < quantity:
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