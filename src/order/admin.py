from django.contrib import admin
from order.models import Order

# Register your models here.
@admin.register(Order)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('id','buyer', 'state','price','shipment','address')
    search_fields = ('buyer', 'state')
    list_filter = ('state',)