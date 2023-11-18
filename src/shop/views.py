from django.shortcuts import render

def welcome(request):
    return render(request, 'index.html', {'user': request.user})

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