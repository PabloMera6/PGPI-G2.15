from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('parts/', views.view_parts, name='parts'),
    path('parts/<int:part_id>/', views.view_part_details, name='part_details')
]