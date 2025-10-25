from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["user", "name", "description", "price", "created_at", "image"]
        read_only_fields = ["user", "created_at"]