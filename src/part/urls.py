from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('parts/', views.view_parts, name='parts'),
]