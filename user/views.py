from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser,Cart
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from .serializer import UserSerializer, CartSerializer
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
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})
        

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [permissions.IsAuthenticated]