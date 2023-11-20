from django.contrib import admin
from order.models import Order
from order.models import OrderProduct
# Register your models here.
@admin.register(Order)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('id','buyer', 'state','price','shipment','address')
    search_fields = ('buyer', 'state')
    list_filter = ('state',)

@admin.register(OrderProduct)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('order','product', 'quantity')
    search_fields = ('order', 'product')
    list_filter = ('order',)