from django import views
from django.urls import path
from . import views
from order.views import administrate,orders,administrate_order,administrate_sells
from users.views import ListUsersView
from newapp.models import Manufacturers as Manufacturer
from django.views.generic import TemplateView



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
    path('administrate/sells/', administrate_sells, name='administrate_sells'),
    path('envios/', TemplateView.as_view(template_name='envios.html'), name='envios'),
    path('pagos/', TemplateView.as_view(template_name='pagos.html'), name='pagos'),


]