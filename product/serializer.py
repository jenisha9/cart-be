from rest_framework import serializers

from product.models import Product, Category, Rate

class ProductSerializer(serializers.Serializer):
    class Meta:
        model=Product
        fields='__all__'

class CategorySerializer(serializers.Serializer):
    class Meta:
        model=Category
        fields='__all__'
        
class RateSerializer(serializers.Serializer):
    class Meta:
        model=Rate
        fields='__all__'