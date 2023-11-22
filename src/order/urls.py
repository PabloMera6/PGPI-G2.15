from django.urls import path
from .views import user_orders
from shop.views import confirmed


urlpatterns = [
    path('user_orders/', user_orders, name='user_orders'),
    path('checkout/confirm/confirmed/<int:order_id>/', confirmed, name='checkout_confirmation'),
]
