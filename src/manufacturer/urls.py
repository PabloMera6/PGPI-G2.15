from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('manufacturers/', views.view_manufacturers, name='manufacturers'),
    path('manufacturers/<int:manufacturer_id>/', views.view_manufacturer_details, name='manufacturer_details')
]