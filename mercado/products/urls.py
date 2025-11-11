from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    #vistas para el crud
    path('', views.home, name='home'),
    path('list/', views.list_products, name='list'),
    path('create/', views.create_product, name='create'),
    path('compare/', views.compare_products, name='compare'),
    path('delete/<int:pk>/', views.delete_product, name='delete'),
    path('edit/<int:pk>/', views.edit_product, name='edit'),
    path('my-products/', views.my_products, name='my_products'),
    
    #mercado pago
    path('create_preference/', views.create_preference, name='create_preference'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('payment/pending/', views.payment_pending, name='payment_pending'),
    
    #urls para ajax
    path('ajax/create/', views.create_product_ajax, name='create_product_ajax'),
    path('ajax/edit/<int:pk>/', views.edit_product_ajax, name='edit_product_ajax'),

    #vistas de carrito
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item'),
]
