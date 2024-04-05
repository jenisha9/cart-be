
from rest_framework import viewsets, filters
from product.models import Product
from product.serializer import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    
    class Meta:
        model= Product
