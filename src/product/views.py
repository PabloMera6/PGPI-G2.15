from django.shortcuts import render
from django.shortcuts import redirect
from .models import Product
from motorcycle.models import Motorcycle
from part.models import Part
from django.contrib.auth.decorators import user_passes_test
from newapp.models import Manufacturers as Manufacturer
from django.contrib import messages
import secrets


# Create your views here.
def view_products(request):
    if request.user.is_authenticated and request.user.is_superuser:
        motos = Motorcycle.objects.all()
        parts = Part.objects.all()
        return render(request, 'products.html', {'motos': motos, 'parts': parts})
    else:
        return redirect('/')

def generate_reference_number():
    reference_number = secrets.token_hex(7).upper()[:15]
    return reference_number

def view_product(request, product_id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(pk=product_id)
        if(product.product_type == 'M'):
            motorcycle = Motorcycle.objects.get(pk=product_id)
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
            return render(request, 'motorcycle_detail2.html', {'motorcycle': motorcycle, 'product': product, 'compatible_parts': compatible_parts,'selected_parts': selected_parts})
        else:
            part = Part.objects.get(pk=product_id)
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
            return render(request, 'part_detail2.html', {'part': part, 'product': product, 'compatible_motorcycles': compatible_motorcycles})
    else:
        return redirect('/')

def new_part(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('name')
            imagen = request.POST.get('imagen')
            category = request.POST.get('category')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            manufacturer_id = request.POST.get('manufacturer')
            try:
                stock = int(stock)
                price = float(price)
            except (ValueError, TypeError):
                return render(request, self.template_name, {'error_message': 'Error al procesar los datos. Asegúrate de ingresar números válidos.'})
            if(price <=0):
                messages.error(request,'El precio no puede ser negativo ni 0')
                return redirect('new_part')
            if(stock<0):
                messages.error(request,'El stock no puede ser negativo')
                return redirect('new_part')
            reference_number = generate_reference_number()
            while True:
                reference_number = generate_reference_number()
                if not Product.objects.filter(reference_number=reference_number).exists():
                    break
            nueva_parte = Part(
                product_type='P',
                name=name,
                photo=imagen,
                category=category,
                stock_quantity=stock,
                price=price,
                manufacturer_id=manufacturer_id,
                reference_number=reference_number
            )
            nueva_parte.save()
            messages.success(request,'Parte creada con éxito')
            return redirect('products')
        manufacturers = Manufacturer.objects.all()
        return render(request, 'new_part.html', {'manufacturers': manufacturers})
    else:
        return redirect('/')

def new_motorcycle(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('name')
            imagen = request.POST.get('imagen')
            category = request.POST.get('category')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            manufacturer_id = request.POST.get('manufacturer')
            carroceria_id = request.POST.get('carroceria')
            carrocerias_compatibles = request.POST.getlist('carroceriac')
            motor_id = request.POST.get('motor')
            motores_compatibles = request.POST.getlist('motorc')
            transmision_id = request.POST.get('transmision')
            transmisiones_compatibles = request.POST.getlist('transmisionc')
            suspension_id = request.POST.get('suspension')
            suspensiones_compatibles = request.POST.getlist('suspensionc')
            ruedas_id = request.POST.get('rueda')
            ruedas_compatibles = request.POST.getlist('ruedac')
            frenos_id = request.POST.get('freno')
            frenos_compatibles = request.POST.getlist('frenoc')
            manillar_id = request.POST.get('manillar')
            manillares_compatibles = request.POST.getlist('manillarc')
            combustible_id = request.POST.get('combustible')
            combustibles_compatibles = request.POST.getlist('combustiblec')
            chasis_id = request.POST.get('chasis')
            chasis_compatibles = request.POST.getlist('chasisc')
            try:
                stock = int(stock)
                price = float(price)
            except (ValueError, TypeError):
                return render(request, self.template_name, {'error_message': 'Error al procesar los datos. Asegúrate de ingresar números válidos.'})
            if(price <=0):
                messages.error(request,'El precio no puede ser negativo ni 0')
                return redirect('new_part')
            if(stock<0):
                messages.error(request,'El stock no puede ser negativo')
                return redirect('new_part')
            reference_number = generate_reference_number()
            while True:
                reference_number = generate_reference_number()
                if not Product.objects.filter(reference_number=reference_number).exists():
                    break
            nueva_moto = Motorcycle(
                product_type='M',
                name=name,
                photo=imagen,
                category=category,
                stock_quantity=stock,
                price=price,
                manufacturer_id=manufacturer_id,
                reference_number=reference_number,
                selected_carrocería_id=carroceria_id,

                selected_motor_id=motor_id,
                selected_transmision_id=transmision_id,
                selected_suspension_id=suspension_id,
                selected_ruedas_id=ruedas_id,
                selected_frenos_id=frenos_id,
                selected_manillar_id=manillar_id,
                selected_combustible_id=combustible_id,
                selected_chasis_id=chasis_id

            )
            nueva_moto.save()
            nueva_moto.compatible_carroceria.set(carrocerias_compatibles)
            nueva_moto.compatible_carroceria.add(carroceria_id)
            nueva_moto.compatible_motor.set(motores_compatibles)
            nueva_moto.compatible_motor.add(motor_id)
            nueva_moto.compatible_transmision.set(transmisiones_compatibles)
            nueva_moto.compatible_transmision.add(transmision_id)
            nueva_moto.compatible_suspension.set(suspensiones_compatibles)
            nueva_moto.compatible_suspension.add(suspension_id)
            nueva_moto.compatible_ruedas.set(ruedas_compatibles)
            nueva_moto.compatible_ruedas.add(ruedas_id)
            nueva_moto.compatible_frenos.set(frenos_compatibles)
            nueva_moto.compatible_frenos.add(frenos_id)
            nueva_moto.compatible_manillar.set(manillares_compatibles)
            nueva_moto.compatible_manillar.add(manillar_id)
            nueva_moto.compatible_combustible.set(combustibles_compatibles)
            nueva_moto.compatible_combustible.add(combustible_id)
            nueva_moto.compatible_chasis.set(chasis_compatibles)
            nueva_moto.compatible_chasis.add(chasis_id)
            nueva_moto.save()
            messages.success(request,'Moto creada con éxito')
            return redirect('products')
        carrocerias = Part.objects.filter(category='Carrocería')
        motores = Part.objects.filter(category='Motor')
        transmisiones = Part.objects.filter(category='Transmisión')
        suspensiones = Part.objects.filter(category='Suspensión')
        ruedas = Part.objects.filter(category='Ruedas')
        frenos = Part.objects.filter(category='Frenos')
        manillares = Part.objects.filter(category='Manillar')
        combustibles = Part.objects.filter(category='Sistema de combustible')
        chasis = Part.objects.filter(category='Chasis')
        manufacturers = Manufacturer.objects.all()
        return render(request, 'new_motorcycle.html', {'manufacturers': manufacturers, 'carrocerias': carrocerias, 'motores': motores, 'transmisiones': transmisiones, 'suspensiones': suspensiones, 'ruedas': ruedas, 'frenos': frenos, 'manillares': manillares, 'combustibles': combustibles, 'chasis': chasis})
    else:
        return redirect('/')

def edit_part(request, part_id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('name')
            imagen = request.POST.get('imagen')
            category = request.POST.get('category')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            manufacturer_id = request.POST.get('manufacturer')
            try:
                stock = int(stock)
                price = float(price)
            except (ValueError, TypeError):
                return render(request, self.template_name, {'error_message': 'Error al procesar los datos. Asegúrate de ingresar números válidos.'})
            if(price <=0):
                messages.error(request,'El precio no puede ser negativo ni 0')
                return redirect('new_part')
            if(stock<0):
                messages.error(request,'El stock no puede ser negativo')
                return redirect('new_part')
            part = Part.objects.get(pk=part_id)
            part.name = name
            part.photo = imagen
            part.category = category
            part.stock_quantity = stock
            part.price = price
            part.manufacturer_id = manufacturer_id
            part.save()
            messages.success(request,'Parte editada con éxito')
            return redirect('products')
        part = Part.objects.get(pk=part_id)
        manufacturers = Manufacturer.objects.all()
        return render(request, 'edit_part.html', {'manufacturers': manufacturers, 'part': part})
    else:
        return redirect('/')

def edit_motorcycle(request, motorcycle_id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('name')
            imagen = request.POST.get('imagen')
            category = request.POST.get('category')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            manufacturer_id = request.POST.get('manufacturer')
            carroceria_id = request.POST.get('carroceria')
            carrocerias_compatibles = request.POST.getlist('carroceriac')
            motor_id = request.POST.get('motor')
            motores_compatibles = request.POST.getlist('motorc')
            transmision_id = request.POST.get('transmision')
            transmisiones_compatibles = request.POST.getlist('transmisionc')
            suspension_id = request.POST.get('suspension')
            suspensiones_compatibles = request.POST.getlist('suspensionc')
            ruedas_id = request.POST.get('rueda')
            ruedas_compatibles = request.POST.getlist('ruedac')
            frenos_id = request.POST.get('freno')
            frenos_compatibles = request.POST.getlist('frenoc')
            manillar_id = request.POST.get('manillar')
            manillares_compatibles = request.POST.getlist('manillarc')
            combustible_id = request.POST.get('combustible')
            combustibles_compatibles = request.POST.getlist('combustiblec')
            chasis_id = request.POST.get('chasis')
            chasis_compatibles = request.POST.getlist('chasisc')
            try:
                stock = int(stock)
                price = float(price)
            except (ValueError, TypeError):
                return render(request, self.template_name, {'error_message': 'Error al procesar los datos. Asegúrate de ingresar números válidos.'})
            if(price <=0):
                messages.error(request,'El precio no puede ser negativo ni 0')
                return redirect('new_part')
            if(stock<0):
                messages.error(request,'El stock no puede ser negativo')
                return redirect('new_part')
            reference_number = generate_reference_number()
            while True:
                reference_number = generate_reference_number()
                if not Product.objects.filter(reference_number=reference_number).exists():
                    break
            nueva_moto = Motorcycle.objects.get(pk=motorcycle_id)
            nueva_moto.name = name
            nueva_moto.photo = imagen
            nueva_moto.category = category
            nueva_moto.stock_quantity = stock
            nueva_moto.price = price
            nueva_moto.manufacturer_id = manufacturer_id
            nueva_moto.selected_carrocería_id=carroceria_id
            nueva_moto.selected_motor_id=motor_id
            nueva_moto.selected_transmision_id=transmision_id
            nueva_moto.selected_suspension_id=suspension_id
            nueva_moto.selected_ruedas_id=ruedas_id
            nueva_moto.selected_frenos_id=frenos_id
            nueva_moto.selected_manillar_id=manillar_id
            nueva_moto.selected_combustible_id=combustible_id
            nueva_moto.selected_chasis_id=chasis_id
            nueva_moto.compatible_carroceria.clear()
            nueva_moto.compatible_motor.clear()
            nueva_moto.compatible_transmision.clear()
            nueva_moto.compatible_suspension.clear()
            nueva_moto.compatible_ruedas.clear()
            nueva_moto.compatible_frenos.clear()
            nueva_moto.compatible_manillar.clear()
            nueva_moto.compatible_combustible.clear()
            nueva_moto.compatible_chasis.clear()
            nueva_moto.save()
            nueva_moto.compatible_carroceria.set(carrocerias_compatibles)
            nueva_moto.compatible_carroceria.add(carroceria_id)
            nueva_moto.compatible_motor.set(motores_compatibles)
            nueva_moto.compatible_motor.add(motor_id)
            nueva_moto.compatible_transmision.set(transmisiones_compatibles)
            nueva_moto.compatible_transmision.add(transmision_id)
            nueva_moto.compatible_suspension.set(suspensiones_compatibles)
            nueva_moto.compatible_suspension.add(suspension_id)
            nueva_moto.compatible_ruedas.set(ruedas_compatibles)
            nueva_moto.compatible_ruedas.add(ruedas_id)
            nueva_moto.compatible_frenos.set(frenos_compatibles)
            nueva_moto.compatible_frenos.add(frenos_id)
            nueva_moto.compatible_manillar.set(manillares_compatibles)
            nueva_moto.compatible_manillar.add(manillar_id)
            nueva_moto.compatible_combustible.set(combustibles_compatibles)
            nueva_moto.compatible_combustible.add(combustible_id)
            nueva_moto.compatible_chasis.set(chasis_compatibles)
            nueva_moto.compatible_chasis.add(chasis_id)
            nueva_moto.save()
            messages.success(request,'Moto actualizada con éxito')
            return redirect('products')
        moto = Motorcycle.objects.get(pk=motorcycle_id)
        carroceria_id = [i.id for i in moto.compatible_carroceria.all()]
        motores_id = [i.id for i in moto.compatible_motor.all()]
        transmisiones_id = [i.id for i in moto.compatible_transmision.all()]
        suspensiones_id = [i.id for i in moto.compatible_suspension.all()]
        ruedas_id = [i.id for i in moto.compatible_ruedas.all()]
        frenos_id = [i.id for i in moto.compatible_frenos.all()]
        combustibles_id = [i.id for i in moto.compatible_combustible.all()]
        chasis_id = [i.id for i in moto.compatible_chasis.all()]
        manillares_id = [i.id for i in moto.compatible_manillar.all()]
        carrocerias = Part.objects.filter(category='Carrocería')
        motores = Part.objects.filter(category='Motor')
        transmisiones = Part.objects.filter(category='Transmisión')
        suspensiones = Part.objects.filter(category='Suspensión')
        ruedas = Part.objects.filter(category='Ruedas')
        frenos = Part.objects.filter(category='Frenos')
        manillares = Part.objects.filter(category='Manillar')
        combustibles = Part.objects.filter(category='Sistema de combustible')
        chasis = Part.objects.filter(category='Chasis')
        manufacturers = Manufacturer.objects.all()
        return render(request, 'edit_motorcycle.html', {'motorcycle':moto,'manufacturers': manufacturers, 'carrocerias': carrocerias, 'motores': motores, 'transmisiones': transmisiones, 'suspensiones': suspensiones, 'ruedas': ruedas, 'frenos': frenos, 'manillares': manillares, 'combustibles': combustibles, 'chasis': chasis,'carroceria_id':carroceria_id,'motores_id':motores_id,'transmisiones_id':transmisiones_id,'suspensiones_id':suspensiones_id,'ruedas_id':ruedas_id,'frenos_id':frenos_id,'combustibles_id':combustibles_id,'chasis_id':chasis_id,'manillares_id':manillares_id})
    else:
        return redirect('/')