from rest_framework import serializers
from .models import CartLine, CustomUser,Cart
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
    product_id = serializers.PrimaryKeyRelatedField(
        read_only=True
    )  # Field to accept product id from frontend
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = CartLine
        fields = ["product_id", "quantity"]


    