from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Order
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from newapp.models import Manufacturers as Manufacturer
from order.models import Order,OrderProduct
from product.models import Product
from motorcycle.models import Motorcycle
from part.models import Part
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

def user_orders(request):

    if request.user.is_authenticated:

        results = Order.objects.filter(buyer=request.user).order_by('-id')

        results_per_page = 12
        page = request.GET.get('page')
        paginator = Paginator(results, results_per_page)

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return render(request, 'user_orders.html', {'orders': results})
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

        orders_per_page = 24
        page = request.GET.get('page')
        paginator = Paginator(orders, orders_per_page)

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
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

def administrate_sells(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if(Order.objects.all().count() == 0):
            producto_mas_vendido = None
            media_precios = None
            tipo_producto_preferido = None
            fabricante_preferido = None
            tipo_envio_preferido = None
            ciudad_mas_ventas = None
            forma_pago_preferida = None
            cliente_mas_activo = None
            grafica_ventas_por_producto = None
            grafica_ventas_por_tipo = None
            grafica_pedidos_por_estado = None
        else:
            producto_mas_vendido = obtener_producto_mas_vendido()
            media_precios = obtener_media_precios()
            media_precios = round(float(media_precios.replace('€','')), 2)
            tipo_producto_preferido = obtener_tipo_producto_preferido()
            fabricante_preferido = obtener_fabricante_preferido()
            tipo_envio_preferido = obtener_tipo_envio_preferido()
            ciudad_mas_ventas = obtener_ciudad_mas_ventas()
            forma_pago_preferida = obtener_forma_pago_preferida()
            cliente_mas_activo = obtener_cliente_mas_activo()
            # grafica_ventas_por_producto = generar_grafica_ventas_por_producto()
            # grafica_ventas_por_tipo = generar_grafica_ventas_por_tipo()
            # grafica_pedidos_por_estado = generar_grafica_pedidos_por_estado()
        return render(request, 'administrate_sells.html', {
        'producto_mas_vendido': producto_mas_vendido,
        'media_precios': media_precios,
        'tipo_producto_preferido': tipo_producto_preferido,
        'fabricante_preferido': fabricante_preferido,
        'tipo_envio_preferido': tipo_envio_preferido,
        'ciudad_mas_ventas': ciudad_mas_ventas,
        'forma_pago_preferida': forma_pago_preferida,
        'cliente_mas_activo': cliente_mas_activo,
        # 'grafica_ventas_por_producto': grafica_ventas_por_producto,
        # 'grafica_ventas_por_tipo': grafica_ventas_por_tipo,
        # 'grafica_pedidos_por_estado': grafica_pedidos_por_estado,
    })
    else:
        return redirect('/')

def obtener_producto_mas_vendido():
    orders = Order.objects.all()
    order_products = OrderProduct.objects.all()
    products = Product.objects.all()
    product_count = {}
    for product in products:
        product_count[product] = 0
    for order in orders:
        for order_product in order_products:
            if order_product.order == order:
                product_count[order_product.product] += order_product.quantity
    max_count = 0
    max_product = None
    for product in product_count:
        if product_count[product] > max_count:
            max_count = product_count[product]
            max_product = product
    if(max_product.product_type == "M"):
        moto = Motorcycle.objects.get(id=max_product.id)
        return moto
    else:
        part = Part.objects.get(id=max_product.id)
        return part
    

def obtener_media_precios():
    orders = Order.objects.all()
    order_products = OrderProduct.objects.all()
    products = Product.objects.all()
    product_count = {}
    for product in products:
        product_count[product] = 0
    for order in orders:
        for order_product in order_products:
            if order_product.order == order:
                product_count[order_product.product] += order_product.quantity
    total_price = 0
    total_quantity = 0
    for product in product_count:
        total_price += product.price * product_count[product]
        total_quantity += product_count[product]
    return str(total_price / total_quantity) + "€"

def obtener_tipo_producto_preferido():
    orders = Order.objects.all()
    order_products = OrderProduct.objects.all()
    products = Product.objects.all()
    product_count = {}
    for product in products:
        product_count[product] = 0
    for order in orders:
        for order_product in order_products:
            if order_product.order == order:
                product_count[order_product.product] += order_product.quantity
    max_count = 0
    max_product = None
    for product in product_count:
        if product_count[product] > max_count:
            max_count = product_count[product]
            max_product = product
    if(max_product.product_type == "M"):
        return "Motocicleta"
    else:
        return "Parte"

def obtener_fabricante_preferido():
    orders = Order.objects.all()
    order_products = OrderProduct.objects.all()
    products = Product.objects.all()
    product_count = {}
    for product in products:
        product_count[product] = 0
    for order in orders:
        for order_product in order_products:
            if order_product.order == order:
                product_count[order_product.product] += order_product.quantity
    max_count = 0
    max_product = None
    for product in product_count:
        if product_count[product] > max_count:
            max_count = product_count[product]
            max_product = product
    return max_product.manufacturer.name

def obtener_tipo_envio_preferido():
    orders = Order.objects.all()
    order_count = {}
    for order in orders:
        order_count[order.shipment] = 0
    for order in orders:
        order_count[order.shipment] += 1
    max_count = 0
    max_order = None
    for order in order_count:
        if order_count[order] > max_count:
            max_count = order_count[order]
            max_order = order
    return max_order    

def obtener_ciudad_mas_ventas():
    orders = Order.objects.all()
    order_count = {}
    for order in orders:
        order_count[order.city] = 0
    for order in orders:
        order_count[order.city] += 1
    max_count = 0
    max_order = None
    for order in order_count:
        if order_count[order] > max_count:
            max_count = order_count[order]
            max_order = order
    return max_order

def obtener_forma_pago_preferida():
    orders = Order.objects.all()
    order_count = {}
    for order in orders:
        order_count[order.payment] = 0
    for order in orders:
        order_count[order.payment] += 1
    max_count = 0
    max_order = None
    for order in order_count:
        if order_count[order] > max_count:
            max_count = order_count[order]
            max_order = order
    return max_order

def obtener_cliente_mas_activo():
    orders = Order.objects.all()
    order_count = {}
    for order in orders:
        order_count[order.buyer_name] = 0
    for order in orders:
        order_count[order.buyer_name] += 1
    max_count = 0
    max_order = None
    for order in order_count:
        if order_count[order] > max_count:
            max_count = order_count[order]
            max_order = order
    return max_order

# def generar_grafica_ventas_por_producto():
#     orders = Order.objects.all()
#     order_products = OrderProduct.objects.all()
#     products = Product.objects.all()
#     product_count = {}

#     for product in products:
#         product_count[product] = 0

#     for order in orders:
#         for order_product in order_products:
#             if order_product.order == order:
#                 product_count[order_product.product] += order_product.quantity

#     labels = []
#     sizes = []

#     for product in product_count:
#         if product.product_type == "M":
#             moto = Motorcycle.objects.get(id=product.id)
#             name = moto.name
#         else:
#             part = Part.objects.get(id=product.id)
#             name = part.name

#         if product_count[product] > 0:
#             labels.append(name)
#             sizes.append(product_count[product])

#     fig, ax = plt.subplots()
#     bars = ax.bar(labels, sizes, color='blue')
#     for bar, size in zip(bars, sizes):
#         height = bar.get_height()
#         ax.annotate(f'{size}',
#                     xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 3),
#                     textcoords="offset points",
#                     ha='center', va='bottom')
    
#     ax.set_title("Ventas por producto")
#     ax.set_xlabel("Productos")
#     ax.set_ylabel("Cantidad vendida")
#     plt.savefig('order/static/images/ventas_por_producto.png')
#     plt.close()
    

# def generar_grafica_ventas_por_tipo():
#     orders = Order.objects.all()
#     order_products = OrderProduct.objects.all()
#     products = Product.objects.all()
#     product_count = {}
#     for product in products:
#         product_count[product] = 0
#     for order in orders:
#         for order_product in order_products:
#             if order_product.order == order:
#                 product_count[order_product.product] += order_product.quantity
#     motos_count = 0
#     parts_count = 0
#     for product in product_count:
#         if product.product_type == "M":
#             motos_count += product_count[product]
#         else:
#             parts_count += product_count[product]
#     labels = 'Motocicletas', 'Partes'
#     sizes = [motos_count, parts_count]
#     fig1, ax1 = plt.subplots()
#     wedges, texts, autotexts = ax1.pie(
#         sizes,
#         labels=labels,
#         autopct='%1.1f%%',
#         startangle=90,
#         textprops=dict(color="black")
#     )
#     legend_labels = [f'{label} ({size})' for label, size in zip(labels, sizes)]
#     ax1.legend(wedges, legend_labels, title="Tipos de Producto", loc="center", bbox_to_anchor=(0.7, 0.5, 0.5, 1))
#     ax1.axis('equal')
#     plt.savefig('order/static/images/ventas_por_tipo.png')
#     plt.close()

# def generar_grafica_pedidos_por_estado():
#     orders = Order.objects.all()
#     order_count = {}
#     for order in orders:
#         order_count[order.state] = 0
#     for order in orders:
#         order_count[order.state] += 1
#     labels = []
#     sizes = []
#     for order in order_count:
#         labels.append(order)
#         sizes.append(order_count[order])
#     fig1, ax1 = plt.subplots()
#     wedges, texts, autotexts = ax1.pie(
#         sizes,
#         labels=labels,
#         autopct='%1.1f%%',
#         startangle=90,
#         textprops=dict(color="black")
#     )
#     legend_labels = [f'{label} ({size})' for label, size in zip(labels, sizes)]
#     ax1.legend(wedges, legend_labels, title="Estados de Pedido", loc="center", bbox_to_anchor=(0.7, 0.5, 0.5, 1))
#     ax1.axis('equal')
#     plt.savefig('order/static/images/pedidos_por_estado.png')
#     plt.close()