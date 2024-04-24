from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
