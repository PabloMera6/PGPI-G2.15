from django.contrib import admin
from motorcycle.models import Motorcycle

# Register your models here.
@admin.register(Motorcycle)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('name','brand', 'photo')
    search_fields = ('name', 'brand')
    list_filter = ('brand',)