from django.contrib import admin
from product.models import Product

# Register your models here.
@admin.register(Product)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('reference_number','product_type', 'price')
    search_fields = ('price', 'product_type')
    list_filter = ('reference_number',)