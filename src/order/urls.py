from django.urls import path
from .views import user_orders
from shop.views import confirmed
from .views import administrate
from .views import orders


urlpatterns = [
    path('user_orders/', user_orders, name='user_orders'),
    path('checkout/confirm/confirmed/<uuid:order_id>/', confirmed, name='checkout_confirmation'),
]
