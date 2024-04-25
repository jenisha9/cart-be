from product.models import Product
from product.serializer import ProductSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework import status

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

    @action(detail=False, methods=["GET"], url_path="get-from-cart")
    def get_from_cart(self, request):
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        cart_lines = cart.cart_lines.all()

        serialized_cart = []
        for cart_line in cart_lines:
            serialized_cart_line = {
                'product': ProductSerializer(cart_line.product).data,  
                'quantity': cart_line.quantity
            }
            serialized_cart.append(serialized_cart_line)

        return Response(serialized_cart)
    
    @action(detail=False, methods=["POST"], url_path="add-to-cart")
    def add_to_cart(self, request):
        user = request.user
        validate = CartSerializer(data=request.data)
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity",1)
        product = Product.objects.get(pk=product_id)
        cart = Cart.objects.get_or_create(user=user)[0]
        
        cart_line_qs = user.cart.cart_lines.filter(product=product)
        if cart_line_qs.exists():
            cart_line = cart_line_qs.first()
            cart_line.quantity += quantity
            cart_line.save()
        else:

            cart_line = CartLine.objects.create(
                product=product, cart=cart, quantity=quantity
            )
        serializer=CartSerializer(cart_line)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], url_path="remove-from-cart")
    def remove_from_cart(self, request):
        user = request.user
        product_id = request.data.get("product_id")

        try:
            cart_line = user.cart.cart_lines.get(product_id=product_id)
            cart_line.delete()
            return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except CartLine.DoesNotExist:
            return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)