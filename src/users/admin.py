from django.contrib import admin
from users.models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class TuModeloAdmin(admin.ModelAdmin):
    list_display = ('email','full_name', 'phone','address')  # Campos que se mostrarán en la lista
    search_fields = ('phone', 'address')  # Campos que se pueden buscar
    list_filter = ('address',)