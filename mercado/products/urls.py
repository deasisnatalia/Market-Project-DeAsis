from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.list_products, name='list'),
    path('create/', views.create_product, name='create'),
    path('compare/', views.compare_products, name='compare'),
]