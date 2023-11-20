from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('motorcycles/', views.view_motorcycles, name='motorcycles'),
    path('motorcycles/<int:motorcycle_id>/', views.view_motorcycle_details, name='motorcycle_details')
]