from rest_framework import serializers
from .models import CustomUser,Cart
# from product.serializer import ProductSerializer
from rest_framework.response import Response
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs={
            'password':{'write_only':True}
        }
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'user', 'added_date']
    
    def destroy(self,request,pk):
        try:
            cart=Cart.objects.get(pk=pk)
            cart.delete()
            return Response({'message':'Deleted'})
        except Cart.DoesNotExist:
            return Response({'message':'Cart not found'})


    