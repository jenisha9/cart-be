from product.models import Product
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework.decorators import action

from .models import Cart, CartLine, CustomUser
from .serializer import CartSerializer, UserSerializer


class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        user=CustomUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed ({'email': 'Invalid Email!'})
        elif not user.check_password(password):
            raise AuthenticationFailed ({'password': "Invalid Password!"})
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})
        
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})


class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=["POST"], url_path="add-to-cart")
    def add_to_cart(self, request):
        user = request.user
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get("product_id")
            quantity = serializer.validated_data.get("quantity", 1)
            try:
                product = Product.objects.get(pk=product_id)
                cart = Cart.objects.get_or_create(user=user)[0]
                cart_line, created = CartLine.objects.get_or_create(product=product, cart=cart)
                if not created:
                    cart_line.quantity += quantity
                    cart_line.save()
                return Response({"message": "Product added to cart"})
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=404)
        else:
            return Response(serializer.errors, status=400)