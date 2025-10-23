from rest_framework import viewsets
from products.models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        #permite ver/editar productos del usuario logueado
        return Product.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        #asigna autoaticamente el usuario logeado al crear un producto
        serializer.save(user=self.request.user)