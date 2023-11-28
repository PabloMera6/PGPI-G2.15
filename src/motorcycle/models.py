from django.db import models
from product.models import Product
from part.models import Part

class Motorcycle(Product):
    
    TYPE_CHOICES = [
        ('Turismo', 'Turismo'),
        ('Deportivo', 'Deportivo'),
        ('Naked', 'Naked'),
        ('Custom', 'Custom')
    ]

    name = models.CharField(max_length=50)
    photo = models.URLField(blank=True, default="", max_length=200)
    category = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Custom')
    stock_quantity = models.PositiveIntegerField(default=0)

    selected_carrocería = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_carrocería')
    compatible_carroceria = models.ManyToManyField(Part, related_name='compatible_carroceria')

    selected_motor = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_motor')
    compatible_motor = models.ManyToManyField(Part, related_name='compatible_motor')

    selected_transmision = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_transmision')
    compatible_transmision = models.ManyToManyField(Part, related_name='compatible_transmision')

    selected_suspension = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_suspension')
    compatible_suspension = models.ManyToManyField(Part, related_name='compatible_suspension')

    selected_ruedas = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_ruedas')
    compatible_ruedas = models.ManyToManyField(Part, related_name='compatible_ruedas')

    selected_frenos = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_frenos')
    compatible_frenos = models.ManyToManyField(Part, related_name='compatible_frenos')

    selected_manillar = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_manillar')
    compatible_manillar = models.ManyToManyField(Part, related_name='compatible_manillar')

    selected_combustible = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_combustible')
    compatible_combustible = models.ManyToManyField(Part, related_name='compatible_combustible')

    selected_chasis = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_chasis')
    compatible_chasis = models.ManyToManyField(Part, related_name='compatible_chasis')

    def calculate_motorcicle_stock(self):
        self.stock_quantity = min(self.selected_carrocería.stock_quantity, self.selected_motor.stock_quantity, self.selected_transmision.stock_quantity, self.selected_suspension.stock_quantity, self.selected_ruedas.stock_quantity, self.selected_frenos.stock_quantity, self.selected_manillar.stock_quantity, self.selected_combustible.stock_quantity, self.selected_chasis.stock_quantity)
        self.save()
    
    def update_motorcicle_stock(self,value):
        carroceria = self.selected_carrocería
        carroceria.stock_quantity = carroceria.stock_quantity - value
        carroceria.save()
        motor = self.selected_motor
        motor.stock_quantity = motor.stock_quantity - value
        motor.save()
        transmision = self.selected_transmision
        transmision.stock_quantity = transmision.stock_quantity - value
        transmision.save()
        suspension = self.selected_suspension
        suspension.stock_quantity = suspension.stock_quantity - value
        suspension.save()
        ruedas = self.selected_ruedas
        ruedas.stock_quantity = ruedas.stock_quantity - value
        ruedas.save()
        frenos = self.selected_frenos
        frenos.stock_quantity = frenos.stock_quantity - value
        frenos.save()
        manillar = self.selected_manillar
        manillar.stock_quantity = manillar.stock_quantity - value
        manillar.save()
        combustible = self.selected_combustible
        combustible.stock_quantity = combustible.stock_quantity - value
        combustible.save()
        chasis = self.selected_chasis
        chasis.stock_quantity = chasis.stock_quantity - value
        chasis.save()
        self.stock_quantity = min(self.selected_carrocería.stock_quantity, self.selected_motor.stock_quantity, self.selected_transmision.stock_quantity, self.selected_suspension.stock_quantity, self.selected_ruedas.stock_quantity, self.selected_frenos.stock_quantity, self.selected_manillar.stock_quantity, self.selected_combustible.stock_quantity, self.selected_chasis.stock_quantity)
        self.save()

    def __str__(self):
        return self.name

class DerivedMotorcycle(Product):
    base_motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, related_name='base_motorcycle', default=0)
    
    carroceria = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='carroceria', default= 0)
    motor = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selemotor', default= 0)
    transmision = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='transmision', default= 0)
    suspension = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='suspension', default= 0)
    ruedas = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='ruedas', default= 0)
    frenos = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='frenos', default=0)
    manillar = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='manillar', default= 0)
    combustible = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='combustible', default= 0)
    chasis = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='chasis', default= 0)

    def calculate_price(self):
        price = self.motorcycle.price
        price += self.carrocería.price
        price += self.motor.price
        price += self.transmision.price
        price += self.suspension.price
        price += self.ruedas.price
        price += self.frenos.price
        price += self.manillar.price
        price += self.combustible.price
        price += self.chasis.price
        price -= self.motorcycle.selected_carrocería.price
        price -= self.motorcycle.selected_motor.price
        price -= self.motorcycle.selected_transmision.price
        price -= self.motorcycle.selected_suspension.price
        price -= self.motorcycle.selected_ruedas.price
        price -= self.motorcycle.selected_frenos.price
        price -= self.motorcycle.selected_manillar.price
        price -= self.motorcycle.selected_combustible.price
        price -= self.motorcycle.selected_chasis.price

    def __str__(self):
        return self.selected_motorcycle.name