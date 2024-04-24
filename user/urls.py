from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RegisterView, CartView, LogoutView

router = DefaultRouter()
router.register(r'cart', CartView, basename='cart')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]



