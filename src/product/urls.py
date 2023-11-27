from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('administrate/products', views.view_products, name='products'),
    path('administrate/products/<int:product_id>/', views.view_product, name='product'),
    path('administrate/products/parts/new', views.new_part, name='new_part'),
    path('administrate/products/motorcycles/new', views.new_motorcycle, name='new_motorcycle'),
    path('administrate/products/parts/edit/<int:part_id>/', views.edit_part, name='edit_part'),
    path('administrate/products/motorcycles/edit/<int:motorcycle_id>/', views.edit_motorcycle, name='edit_motorcycle'),
]