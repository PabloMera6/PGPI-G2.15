from django import views
from django.urls import path
from . import views
from order.views import administrate,orders,administrate_order
from users.views import ListUsersView
from manufacturer.models import Manufacturer



urlpatterns = [
    path('', views.welcome, name='initial'),
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_cart, name='cart_remove'),
    path('cart/refresh/', views.refresh_cart, name='refresh'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/confirm/', views.confirm, name='confirm'),
    path('checkout/confirm/confirmed/<uuid:order_id>/', views.confirmed, name='confirmed'),
    path('administrate/', administrate, name='administrate'),
    path('administrate/orders/',orders, name='orders'),
    path('administrate/orders/<uuid:order_id>/', administrate_order, name='administrate_order'),
    path('administrate/users/', ListUsersView.as_view(), name='administrate_users'),
]