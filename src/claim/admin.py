from django.contrib import admin
from claim.models import Claim

# Register your models here.
@admin.register(Claim)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('author','date', 'description')  # Campos que se mostrarán en la lista
    search_fields = ('date',)  # Campos que se pueden buscar
    list_filter = ('date',)