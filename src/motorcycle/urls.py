from django import views
from django.urls import path
from . import views
from .views import MotorcycleDetailView
from order.views import check_order_status


urlpatterns = [
    path('motorcycles/', views.view_motorcycles, name='motorcycles'),

    path('motorcycles/config/<int:motorcycle_id>/', views.config, name='motorcycles_config'),

    path('motorcycles/<int:motorcycle_id>/', MotorcycleDetailView.as_view(), name='motorcycle_details'),

    path('check_order_status/', check_order_status, name='check_order_status'),
]