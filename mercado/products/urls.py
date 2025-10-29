from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.list_products, name='list'),
    path('create/', views.create_product, name='create'),
    path('compare/', views.compare_products, name='compare'),
    path('my-products/', views.my_products, name='my_products'),
]