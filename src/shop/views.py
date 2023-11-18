from django.shortcuts import render
from motorcycle.models import Motorcycle
from part.models import Part
import random

def welcome(request):
    motorcycles = Motorcycle.objects.all()
    parts = Part.objects.all()
    combined_list = list(motorcycles) + list(parts)
    random.shuffle(combined_list)
    active_group = combined_list[:3]
    other_groups = [combined_list[i:i+3] for i in range(3, len(combined_list), 3)]

    return render(request, 'index.html', {'user': request.user, 'active': active_group, 'others': other_groups})

def view_cart(request):
        return render(request, 'cart.html')

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart[product_id] = quantity
        else:
            for key, value in self.cart.items():
                if key == product_id:
                    value = value + quantity
                    break
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product.id]
            self.save()

    def decrement(self, product, quantity):
        product_id = str(product.id)
        for key, value in self.cart.items():
            if key == product_id:
                value = value - quantity
                if value <= 0:
                    self.remove()
                break
        self.save()


    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
    
    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True