from django.contrib import admin
from manufacturers.models import Manufacturer

# Register your models here.

@admin.register(Manufacturer)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('name','photo')
    search_fields = ('name',)
    list_filter = ('name',)