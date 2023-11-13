from django.contrib import admin
from part.models import Part

# Register your models here.
@admin.register(Part)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'photo')
    search_fields = ('name', 'category')
    list_filter = ('category',)