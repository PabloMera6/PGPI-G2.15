from django.contrib import admin
from .models import Opinion

@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'product', 'date', 'score')
    search_fields = ('author__username', 'product__name')
    list_filter = ('score', 'date')
    date_hierarchy = 'date'
