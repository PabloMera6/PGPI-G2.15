from django.db import models
from product.models import Product
from part.models import Part

class Motorcycle(Product):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='motorcycle_photos/', null=True, blank=True)
    brand = models.CharField(max_length=50)

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

    selected_electricidad = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_electricidad')
    compatible_electricidad = models.ManyToManyField(Part, related_name='compatible_electricidad')

    selected_manillar = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_manillar')
    compatible_manillar = models.ManyToManyField(Part, related_name='compatible_manillar')

    selected_combustible = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_combustible')
    compatible_combustible = models.ManyToManyField(Part, related_name='compatible_combustible')

    selected_chasis = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='selected_chasis')
    compatible_chasis = models.ManyToManyField(Part, related_name='compatible_chasis')
