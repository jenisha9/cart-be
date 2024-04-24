from django.contrib.auth.models import AbstractUser
from django.db import models
from product.models import Product
from rest_framework.authtoken.models import Token
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        # extra_fields['email']=self.normalize_email(extra_fields['email'])
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email, password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
    
        
        return self.create_user(email, password,**extra_fields)
    
class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def get_or_create_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key

    def __str__(self):
        return self.email

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

class CartLine(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_lines")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
 