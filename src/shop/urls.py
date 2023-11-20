from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='initial'),
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_cart, name='cart_remove'),
    path('cart/refresh/', views.refresh, name='refresh'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/confirm/', views.confirm, name='confirm'),
]