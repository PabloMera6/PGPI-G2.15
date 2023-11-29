from django import views
from django.urls import path
from . import views
from .views import PartDetailView


urlpatterns = [
    path('parts/', views.view_parts, name='parts'),
    path('parts/<int:part_id>/', PartDetailView.as_view(), name='part_details')
]